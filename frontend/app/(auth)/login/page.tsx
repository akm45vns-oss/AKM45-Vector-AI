import type { Metadata } from "next";
import { LoginForm } from "@/components/auth/LoginForm";

export const metadata: Metadata = {
  title: "Sign In — AKM45 Vector AI",
  description: "Sign in to your AKM45 Vector AI account to manage your recruitment pipeline.",
};

export default function LoginPage() {
  return <LoginForm />;
}
