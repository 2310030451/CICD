import { useEffect } from "react";
import { useAuthStore } from "@/store/auth-store";
import { auth, getCurrentUser } from "@/lib/firebase";
import { authApi } from "@/lib/api/auth";
import { User } from "@/types";

export function useAuth() {
  const { user, isAuthenticated, isLoading, setUser, setLoading, logout } =
    useAuthStore();

  useEffect(() => {
    const unsubscribe = auth?.onAuthStateChanged(
      async (firebaseUser) => {
        if (firebaseUser) {
          try {
            const token = await firebaseUser.getIdToken();
            const response = await authApi.verifyToken(token);
            setUser(response.user);
            localStorage.setItem("access_token", response.access_token);
            localStorage.setItem("refresh_token", response.refresh_token);
          } catch (error) {
            console.error("Auth error:", error);
            logout();
          }
        } else {
          logout();
        }
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, [setUser, setLoading, logout]);

  return { user, isAuthenticated, isLoading };
}
