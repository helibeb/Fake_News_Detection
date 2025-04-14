import { NewsAnalyzer } from "@/components/news-analyzer"

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight">Fake News Detector</h1>
          <p className="mt-3 text-xl text-gray-500 sm:mt-4">
            Using Bayesian Decision Theory to identify misinformation
          </p>
        </div>

        <NewsAnalyzer />
      </div>
    </main>
  )
}
