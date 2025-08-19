import moment from "moment";
import "moment/locale/vi";

moment.locale("vi");

export function formatDateFromArray(isoString, options = {}) {
  if (typeof isoString !== "string") return "";

  const date = new Date(isoString);
  if (isNaN(date)) return "";

  const { locale = "vi-VN", includeTime = false } = options;

  const dateOptions = {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    ...(includeTime && {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }),
  };

  return date.toLocaleString(locale, dateOptions);
}


export const formatDate = (input) => {
  if (typeof input === "string") {
    return moment(input).fromNow();
  }

  if (Array.isArray(input)) {
    const [year, month, ...rest] = input;
    const date = new Date(year, month - 1, ...rest);
    return moment(date).fromNow();
  }

  return "";
};