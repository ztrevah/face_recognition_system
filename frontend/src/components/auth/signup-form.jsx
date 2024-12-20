import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useAuthContext } from '../../context/auth-context'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { Input } from '../ui/input'
import { useState } from 'react'
import { Button } from '../ui/button'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'


const formSchema = z.object({
  username: z.string().min(1, {
      message: 'Username is required!'
  }),
  password: z.string().min(1, {
      message: 'Password is required!'
  }),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: 'Confirmed password is not correct.',
  path: ['confirmPassword']
})

const SignUpForm = () => {
    const { signup } = useAuthContext()
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate()
    const searchParams = useSearchParams()
    
    const redirectUrl = searchParams.get('redirect_url') || '/'
    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: '',
            password: '',
            confirmPassword: ''
        }
    })
    const onSubmit = async (values) => {
      const { username, password } = values
        try {
            setIsLoading(true)
            await signup({ username, password })
            form.reset()
            navigate(redirectUrl)
        } catch(err) {
            console.log(err)
        } finally {
            setIsLoading(false)
        }
    }
    return (
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-8'>
            <div className='space-y-8 px-6'>
              <FormField
                control={form.control}
                name='username'
                render={({ field }) => (
                  <FormItem className="w-[400px]">
                    <FormLabel className='text-xs font-bold uppercase'>
                      Username
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        className='border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0 m-0'
                        placeholder='Enter your username'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='text-red-600' />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name='password'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='text-xs font-bold uppercase'>
                        Password
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        type='password'
                        className='border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0'
                        placeholder='Enter your password'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='text-red-600' />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name='confirmPassword'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='text-xs font-bold uppercase'>
                        Confirm your password
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        type='password'
                        className='border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0'
                        placeholder='Enter your password again'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='text-red-600' />
                  </FormItem>
                )}
              />
            </div>
            <div className="w-full text-center">
              <Button disabled={isLoading} variant='default'>
                  Sign up
              </Button>
              <div className='text-md font-medium mt-4'>
                Already have an account? <Link href="/sign-in" className='text-rose-500'>Sign in</Link>
              </div>
            </div>
          </form>
        </Form>
    )
}

export default SignUpForm