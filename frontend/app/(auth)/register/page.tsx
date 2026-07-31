import type { Metadata } from "next";
import { RegisterForm } from "@/components/auth/RegisterForm";

export const metadata: Metadata = {
  title: "Create Account — AKM45 Vector AI",
  description: "Create your free AKM45 Vector AI account. AI-powered recruitment for modern teams.",
};

export default function RegisterPage() {
  return <RegisterForm />;
}
