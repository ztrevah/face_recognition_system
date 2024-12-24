import { useForm } from "react-hook-form";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "../../context/auth-context";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";
import { useState } from "react";
import { Button } from "../ui/button";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

const formSchema = z.object({
  username: z.string().min(1, {
    message: "Username is required!",
  }),
  password: z.string().min(1, {
    message: "Password is required!",
  }),
});

const SignInForm = () => {
  const { signin } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const redirectUrl = searchParams.get("redirect_url") || "/";
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });
  const onSubmit = async (values) => {
    try {
      setIsLoading(true);
      const res = await signin(values);
      setError("");
      form.reset();
      navigate(redirectUrl);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-4">
        <div className="space-y-4 px-6">
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem className="w-[300px]">
                <FormLabel className="text-xs font-bold uppercase">
                  Username
                </FormLabel>
                <FormControl>
                  <Input
                    disabled={isLoading}
                    className="border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0 m-0"
                    placeholder="Enter your username"
                    {...field}
                  />
                </FormControl>
                <FormMessage className="text-red-600" />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem className="w-[300px]">
                <FormLabel className="text-xs font-bold uppercase">
                  Password
                </FormLabel>
                <FormControl>
                  <Input
                    disabled={isLoading}
                    type="password"
                    className="border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0"
                    placeholder="Enter your password"
                    {...field}
                  />
                </FormControl>
                <FormMessage className="text-red-600" />
              </FormItem>
            )}
          />
        </div>
        {error ? (
          <div className="text-red-600 text-sm font-bold text-center">
            {error}
          </div>
        ) : (
          ""
        )}
        <div className="w-full text-center">
          <Button disabled={isLoading} variant="default">
            Sign in
          </Button>
          <div className="text-md font-medium mt-4">
            Don&apos;t have an account?{" "}
            <Link to="/sign-up" className="text-rose-500">
              Sign up
            </Link>
          </div>
        </div>
      </form>
    </Form>
  );
};

export default SignInForm;
