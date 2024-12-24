import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { Input } from "../ui/input";
import { Button } from "../ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";

import { useAuth } from "../../context/auth-context";
import { useToast } from "@/hooks/use-toast";
import { EpSuccessFilled } from "../icons/Icon";

const formSchema = z
  .object({
    username: z.string().min(1, {
      message: "Username is required!",
    }),
    password: z.string().min(1, {
      message: "Password is required!",
    }),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Confirmed password is not correct.",
    path: ["confirmPassword"],
  });

const SignUpForm = () => {
  const { signup } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
      confirmPassword: "",
    },
  });
  const onSubmit = async (values) => {
    const { username, password } = values;
    try {
      setIsLoading(true);
      await signup({ username, password });
      setError("");
      form.reset();
      navigate("/sign-in");
      toast({
        title: (
          <div className="flex items-center">
            <EpSuccessFilled className="h-4 w-4 mr-2 [&>path]:fill-green-500" />
            Successfully sign up
          </div>
        ),
        description: "Now you can sign in to our app.",
        variant: "successful",
        className: "",
      });
    } catch (err) {
      setError(err.message);
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
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
              <FormItem>
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
          <FormField
            control={form.control}
            name="confirmPassword"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-xs font-bold uppercase">
                  Confirm your password
                </FormLabel>
                <FormControl>
                  <Input
                    disabled={isLoading}
                    type="password"
                    className="border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0"
                    placeholder="Enter your password again"
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
            Sign up
          </Button>
          <div className="text-md font-medium mt-4">
            Already have an account?{" "}
            <Link to="/sign-in" className="text-rose-500">
              Sign in
            </Link>
          </div>
        </div>
      </form>
    </Form>
  );
};

export default SignUpForm;
