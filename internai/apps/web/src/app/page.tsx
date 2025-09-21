import { redirect } from 'next/navigation';

export default function Home() {
  // Redirect to dashboard since we have a proper dashboard shell
  redirect('/dashboard');
}
