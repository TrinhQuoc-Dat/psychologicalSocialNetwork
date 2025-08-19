import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { 
  Container, 
  CircularProgress, 
  Typography, 
  Button,
  Box,
  Alert
} from '@mui/material';
import { FaArrowLeft } from 'react-icons/fa';
import SurveyStatsCard from '../components/survey/SurveyStatistics/SurveyStatsCard';
import QuestionStats from '../components/survey/SurveyStatistics/QuestionStats';
import { getSurveyStatistics } from '../services/surveyPostService';

const SurveyStatsPage = () => {
  const { surveyPostId } = useParams();
  const navigate = useNavigate();
  const { token, role } = useSelector(state => state.auth);
  const [statsData, setStatsData] = useState({
    statistics: [],
    participantCount: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const currentUser = useSelector((state) => state.auth.user);

  const isAdmin = currentUser?.role === "ADMIN";
  // const isOwner = currentUser?.id === post.user.id;



  useEffect(() => {
    fetchStats();
    
  }, [surveyPostId, role]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getSurveyStatistics(surveyPostId);
      setStatsData(data);
      console.log("setStatsData", data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Không thể tải thống kê. Vui lòng thử lại sau.');
    } finally {
      setLoading(false);
    }
  };
    console.log("Grouped", groupByQuestion(statsData.statistics));
  const handleBack = () => {
    navigate(-1);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button 
        startIcon={<FaArrowLeft />} 
        onClick={handleBack}
        sx={{ mb: 3 }}
        variant="outlined"
      >
        Quay lại
      </Button>

      <Typography variant="h4" component="h1" sx={{ mb: 4 }}>
        Thống kê khảo sát chi tiết
      </Typography>

      {loading ? (
        <Box display="flex" justifyContent="center" py={8}>
          <CircularProgress size={60} />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      ) : (
        <>
          <SurveyStatsCard 
            statistics={statsData.statistics} 
            participantCount={statsData.participantCount} 
          />
          
          <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', gap: 4 }}>
            {groupByQuestion(statsData.statistics).map((question) => (
              <QuestionStats 
                key={question.questionId} 
                question={question}
                participantCount={statsData.participantCount}
              />
            ))}
          </Box>
        </>
      )}
    </Container>
  );
};

// Hàm nhóm các option theo question
const groupByQuestion = (stats) => {
  if (!stats) return [];
  
  const questionsMap = new Map();
  
  stats.forEach((item) => {
    if (!questionsMap.has(item.questionId)) {
      questionsMap.set(item.questionId, {
        questionId: item.questionId,
        questionText: item.question,
        options: []
      });
    }
    questionsMap.get(item.questionId).options.push({
      optionId: item.optionId,
      optionText: item.optionText,
      totalSelected: item.totalSelected
    });
  });
  
  return Array.from(questionsMap.values());
};


export default SurveyStatsPage;


// {
//   "participantCount": 42,
//   "statistics": [
//     {
//       "questionId": 1,
//       "question": "Bạn có cảm thấy áp lực khi học không?",
//       "optionId": 5,
//       "optionText": "Có",
//       "totalSelected": 30
//     },
//     {
//       "questionId": 1,
//       "question": "Bạn có cảm thấy áp lực khi học không?",
//       "optionId": 6,
//       "optionText": "Không",
//       "totalSelected": 12
//     },
//     ...
//   ]
// }