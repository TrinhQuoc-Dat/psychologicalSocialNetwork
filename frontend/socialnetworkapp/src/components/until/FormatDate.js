import { formatDistanceToNow } from "date-fns";
import { vi } from "date-fns/locale"

export const formatDateNow = (time) => {
    // Nếu backend trả về "2025-09-02 12:00:00", convert sang ISO
    if (typeof time === "string" && time.includes(" ")) {
        time = time.replace(" ", "T") + "Z";
    }

    const date = new Date(time);
    if (isNaN(date)) return "Thời gian không hợp lệ";

    return formatDistanceToNow(date, {
        addSuffix: true,
        locale: vi,
    });
}
