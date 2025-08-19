import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getPostById, getSurveyById } from "../services/postService";
import {
  checkUserHasAnsweredSurvey,
  selectMultipleSurveyOptions,
} from "../services/surveyPostService";
import { useSelector } from "react-redux";
import { formatDateFromArray } from "../app/utils/dateUtils";
import { motion } from "framer-motion";
import { FiArrowLeft, FiCheck, FiCheckCircle, FiClock, FiLock } from "react-icons/fi";
import ProgressBar from "../components/ProgressBar";

const SurveyDetailPage = () => {
  const { postId } = useParams();
  const navigate = useNavigate();
  const token = useSelector((state) => state.auth.token);
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [responses, setResponses] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [hasAnswered, setHasAnswered] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [surveyExpired, setSurveyExpired] = useState(false);


  useEffect(() => {
    const fetchSurvey = async () => {
      try {
        const [answeredStatus, surveyData] = await Promise.all([
          checkUserHasAnsweredSurvey(postId),
          getSurveyById(postId),
        ]);
        console.log("surveyData==> ", surveyData);
        setHasAnswered(answeredStatus);
        setPost(surveyData);

        // Check if survey is expired
        if (surveyData.status === "EXPIRED") {
          setSurveyExpired(true);
        }

        if (surveyData.questions_read) {
          const initialResponses = {};
          surveyData.questions_read.forEach((q) => {
            initialResponses[q.id] = q.multi_choice ? [] : null;
          });
          console.log("initialResponses", initialResponses);
          setResponses(initialResponses);
          calculateProgress(
            initialResponses,
            surveyData.questions_read.length
          );
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSurvey();
  }, [postId, token]);

  const calculateProgress = (currentResponses, totalQuestions) => {
    const answeredQuestions = Object.values(currentResponses).filter(
      (response) =>
        response !== null &&
        (Array.isArray(response) ? response.length > 0 : true)
    ).length;
    const newProgress = (answeredQuestions / totalQuestions) * 100;
    setProgress(newProgress);
  };

  const handleResponseChange = (questionId, optionIndex, isMulti, checked) => {
    setResponses((prev) => {
      let newResponses;
      if (isMulti) {
        const newArray = [...(prev[questionId] || [])];
        if (checked) {
          newArray.push(optionIndex);
        } else {
          const index = newArray.indexOf(optionIndex);
          if (index > -1) {
            newArray.splice(index, 1);
          }
        }
        newResponses = { ...prev, [questionId]: newArray };
      } else {
        newResponses = { ...prev, [questionId]: optionIndex };
      }

      setTimeout(() => {
        calculateProgress(newResponses, post.questions_read.length);
      }, 0);

      return newResponses;
    });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (surveyExpired) {
      alert("Khảo sát này đã hết hạn và không thể gửi câu trả lời.");
      return;
    }

    setSubmitting(true);

    try {
      const answers = post.questions_read
        .map((question) => {
          const selectedOptions = responses[question.id];
          return {
            questionId: question.id,
            optionIds: Array.isArray(selectedOptions)
              ? selectedOptions.map((index) => question.options[index].id)
              : selectedOptions !== null
                ? [question.options[selectedOptions].id]
                : [],
          };
        })
        .filter((answer) => answer.optionIds.length > 0);

      console.log("answers", answers);

      if (answers.length !== post.questions_read.length) {
        throw new Error("Vui lòng trả lời tất cả các câu hỏi trước khi gửi");
      }

      await selectMultipleSurveyOptions(answers, postId);

      setHasAnswered(true);
      setSubmitSuccess(true);

      setTimeout(() => {
        setSubmitSuccess(false);
      }, 3000);
    } catch (err) {
      console.error("Lỗi khi gửi khảo sát:", err);
      alert(
        err.response?.data?.message ||
        err.message ||
        "Có lỗi xảy ra khi gửi khảo sát"
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-lg font-medium text-gray-700">
            Đang tải khảo sát...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center p-6 max-w-md bg-white rounded-lg shadow-md">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            Đã xảy ra lỗi
          </h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center p-6 max-w-md bg-white rounded-lg shadow-md">
          <div className="text-gray-500 text-4xl mb-4">🔍</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            Không tìm thấy khảo sát
          </h2>
          <p className="text-gray-600 mb-4">
            Khảo sát bạn đang tìm kiếm không tồn tại hoặc đã bị xóa.
          </p>
          <button
            onClick={() => navigate("home")}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Quay lại
          </button>
        </div>
      </div>
    );
  }

  const survey = post;
  const endTimeFormatted = formatDateFromArray(survey.end_time, {
    includeTime: true,
  });
  const [dateStr, timeStr] = endTimeFormatted.split(", ");

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Back button */}
        <button
          onClick={() => navigate('/home')}
          className="flex items-center text-blue-600 hover:text-blue-800 mb-6 transition"
        >
          <FiArrowLeft className="mr-2" />
          Quay lại
        </button>

        {/* Survey header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-xl shadow-sm p-6 mb-6"
        >
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-3">
            {post.content}
          </h1>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
            <div className={`flex items-center px-3 py-1 rounded-full ${surveyExpired ? "bg-red-50 text-red-600" : "bg-blue-50 text-blue-600"
              }`}>
              <FiClock className="mr-2" />
              <span className="font-medium">
                {surveyExpired ? "Đã kết thúc" : "Kết thúc"}: {dateStr}
              </span>
            </div>

            <div className="flex items-center bg-green-50 px-3 py-1 rounded-full text-green-600">
              <FiCheck className="mr-2" />
              <span className="font-medium">
                {survey.questions_read.length} câu hỏi
              </span>
            </div>

            {surveyExpired && (
              <div className="flex items-center bg-red-50 px-3 py-1 rounded-full text-red-600">
                <FiLock className="mr-2" />
                <span className="font-medium">Đã hết hạn</span>
              </div>
            )}
          </div>
        </motion.div>

        {submitSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6"
          >
            <div className="flex items-center">
              <FiCheckCircle className="mr-2" />
              <span>Gửi khảo sát thành công!</span>
            </div>
          </motion.div>
        )}

        {hasAnswered || surveyExpired ? (
          <>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`border rounded-xl p-6 mb-6 ${surveyExpired
                ? "bg-red-50 border-red-200 text-red-800"
                : "bg-green-50 border-green-200 text-green-800"
                }`}
            >
              <div className="flex items-center">
                {surveyExpired ? (
                  <FiLock className="text-red-500 text-2xl mr-3" />
                ) : (
                  <FiCheckCircle className="text-green-500 text-2xl mr-3" />
                )}
                <div>
                  <h3 className="text-lg font-medium">
                    {surveyExpired
                      ? "Khảo sát này đã hết hạn"
                      : "Bạn đã hoàn thành khảo sát này"}
                  </h3>
                  <p>
                    {surveyExpired
                      ? "Bạn không thể gửi câu trả lời cho khảo sát đã hết hạn."
                      : "Cảm ơn bạn đã dành thời gian tham gia khảo sát."}
                  </p>
                </div>
              </div>
            </motion.div>

            <div className="bg-white rounded-xl shadow-sm p-6 text-center">
              <p className="text-gray-600">
                {surveyExpired
                  ? "Khảo sát đã kết thúc vào ngày " + dateStr
                  : "Bạn có thể xem kết quả khảo sát khi chủ khảo sát công bố."}
              </p>
            </div>
          </>
        ) : (
          <>
            {/* Progress bar */}
            <div className="mb-8">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Tiến độ hoàn thành
                </span>
                <span className="text-sm font-medium text-blue-600">
                  {Math.round(progress)}%
                </span>
              </div>
              <ProgressBar value={progress} />
            </div>

            {/* Survey form */}
            <motion.form
              onSubmit={handleSubmit}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1, duration: 0.3 }}
              className="space-y-6"
            >
              {survey.questions_read.map((question, qIndex) => (
                <motion.div
                  key={question.id || qIndex}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + qIndex * 0.05 }}
                  className="bg-white rounded-xl shadow-sm overflow-hidden"
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start">
                      <h3 className="text-lg font-medium text-gray-800 mb-4">
                        <span className="text-blue-600 mr-2">
                          Câu {qIndex + 1}:
                        </span>
                        {question.question}
                      </h3>
                      {question.multi_choice && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          Nhiều lựa chọn
                        </span>
                      )}
                    </div>

                    <div className="space-y-3">
                      {question.options.map((option, oIndex) => (
                        <div
                          key={option.id}
                          className={`p-3 rounded-lg border transition ${(
                            question.multi_choice
                              ? responses[qIndex]?.includes(oIndex)
                              : responses[qIndex] === oIndex
                          )
                            ? "border-blue-500 bg-blue-50"
                            : "border-gray-200 hover:border-gray-300"
                            }`}
                        >
                          <label className="flex items-center cursor-pointer">
                            <input
                              type={question.multi_choice ? "checkbox" : "radio"}
                              className={`form-${question.multi_choice ? "checkbox" : "radio"
                                } text-blue-600 focus:ring-blue-500 h-4 w-4`}
                              checked={
                                question.multi_choice
                                  ? responses[question.id]?.includes(oIndex)
                                  : responses[question.id] === oIndex
                              }
                              onChange={(e) =>
                                handleResponseChange(
                                  question.id,
                                  oIndex,
                                  question.multi_choice,
                                  e.target.checked
                                )
                              }
                            />
                            <span className="ml-3 text-gray-700">
                              {option.option_text}
                            </span>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              ))}

              {/* Submit button */}
              <div className="sticky bottom-0 bg-white py-4 border-t border-gray-200">
                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={submitting || progress < 100 || surveyExpired}
                    className={`px-6 py-3 rounded-lg font-medium transition ${submitting
                      ? "bg-blue-400 cursor-not-allowed"
                      : progress < 100 || surveyExpired
                        ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                        : "bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg"
                      }`}
                  >
                    {submitting ? (
                      <span className="flex items-center">
                        <svg
                          className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          ></circle>
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          ></path>
                        </svg>
                        Đang gửi...
                      </span>
                    ) : (
                      "Gửi khảo sát"
                    )}
                  </button>
                </div>
              </div>
            </motion.form>
          </>
        )}
      </div>
    </div>
  );
};

export default SurveyDetailPage;