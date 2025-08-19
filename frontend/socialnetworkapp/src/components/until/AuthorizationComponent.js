const Authorization = () => {
    return {
       Authorization: `Bearer ${localStorage.getItem("token")}` || null
    }
}

export const AuthorizationFromData = () => {
    return {
       Authorization: `Bearer ${localStorage.getItem("token")}` || null,
        "Content-Type": "multipart/form-data",
    }
}

export default Authorization;