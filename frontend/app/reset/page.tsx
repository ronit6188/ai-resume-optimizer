import { EnvelopeIcon } from "@heroicons/react/24/outline";
import Link from "next/link";

export default function ResetPage() {
  return (
    <main className="mx-auto grid min-h-[calc(100vh-73px)] max-w-7xl place-items-center px-4 py-12 sm:px-6 lg:px-8">
      <section className="w-full max-w-md rounded-lg border border-ink/10 bg-white p-6 text-center shadow-panel">
        <div className="mx-auto grid h-12 w-12 place-items-center rounded-md bg-mist text-pine">
          <EnvelopeIcon className="h-6 w-6" />
        </div>
        <h1 className="mt-4 text-2xl font-semibold text-ink">Password reset</h1>
        <p className="mt-3 text-sm leading-6 text-ink/65">
          Email delivery is not connected yet. Use signup or login while SMTP settings are added.
        </p>
        <Link
          className="focus-ring mt-6 inline-flex rounded-md bg-pine px-4 py-3 text-sm font-semibold text-white hover:bg-ink"
          href="/login"
        >
          Back to login
        </Link>
      </section>
    </main>
  );
}
