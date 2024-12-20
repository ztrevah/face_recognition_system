import authServices from "@/services/auth"

export const currentUser = async () => {
    try {
        const res = await authServices.verify()
        return res.data
    } catch(err) {
        return null
    }
}