"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { AlertCircle, CheckCircle, Info } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

type AnalysisResult = {
  prediction: "REAL" | "FAKE"
  probability: number
  features: {
    name: string
    contribution: number
    description: string
  }[]
}

export function NewsAnalyzer() {
  const [newsText, setNewsText] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyzeNews = async () => {
    if (!newsText.trim()) {
      setError("Please enter some text to analyze")
      return
    }

    setIsAnalyzing(true)
    setError(null)

    try {
      // In a real implementation, this would call your Python backend
      const response = await fetch("http://localhost:8000/api/analyze", {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify({ text: newsText }),
       });

      // if (!response.ok) throw new Error("Failed to analyze text");
      // const data = await response.json();
      // setResult(data);

      // For demonstration, we'll simulate a response
      setTimeout(() => {
        // Simulate backend response
        const mockResult: AnalysisResult = {
          prediction: Math.random() > 0.5 ? "REAL" : "FAKE",
          probability: 0.2 + Math.random() * 0.6,
          features: [
            {
              name: "Emotional Language",
              contribution: 0.35,
              description: "High emotional content often indicates potential bias",
            },
            {
              name: "Source Credibility",
              contribution: 0.25,
              description: "Analysis of cited sources and their reliability",
            },
            {
              name: "Statistical Consistency",
              contribution: 0.2,
              description: "Evaluation of numerical claims and statistics",
            },
            {
              name: "Writing Style",
              contribution: 0.2,
              description: "Linguistic patterns common in misleading content",
            },
          ],
        }

        setResult(mockResult)
        setIsAnalyzing(false)
      }, 2000)
    } catch (err) {
      setError("Failed to analyze the news. Please try again.")
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>News Article Analysis</CardTitle>
          <CardDescription>Paste a news article or headline to analyze its credibility</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            placeholder="Paste news article text here..."
            className="min-h-[200px]"
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
          />
        </CardContent>
        <CardFooter>
          <Button onClick={analyzeNews} disabled={isAnalyzing} className="w-full">
            {isAnalyzing ? "Analyzing..." : "Analyze Text"}
          </Button>
        </CardFooter>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {isAnalyzing && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-sm text-muted-foreground mb-2">Analyzing with Bayesian Decision Theory...</p>
            <Progress value={45} className="h-2" />
          </CardContent>
        </Card>
      )}

      {result && (
        <Card className={result.prediction === "FAKE" ? "border-red-200 bg-red-50" : "border-green-200 bg-green-50"}>
          <CardHeader>
            <CardTitle className="flex items-center">
              {result.prediction === "FAKE" ? (
                <>
                  <AlertCircle className="mr-2 h-5 w-5 text-red-500" />
                  <span className="text-red-700">Likely Fake News</span>
                </>
              ) : (
                <>
                  <CheckCircle className="mr-2 h-5 w-5 text-green-500" />
                  <span className="text-green-700">Likely Reliable</span>
                </>
              )}
            </CardTitle>
            <CardDescription>Confidence: {Math.round(result.probability * 100)}%</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <h3 className="font-medium text-sm">Key factors in this analysis:</h3>
              <div className="space-y-3">
                {result.features.map((feature, index) => (
                  <div key={index} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>{feature.name}</span>
                      <span>{Math.round(feature.contribution * 100)}%</span>
                    </div>
                    <Progress value={feature.contribution * 100} className="h-1" />
                    <p className="text-xs text-muted-foreground">{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Alert>
              <Info className="h-4 w-4" />
              <AlertTitle>About Bayesian Analysis</AlertTitle>
              <AlertDescription className="text-xs">
                This analysis uses Bayesian Decision Theory to calculate the probability of an article being fake news
                based on multiple textual features and prior knowledge of misinformation patterns.
              </AlertDescription>
            </Alert>
          </CardFooter>
        </Card>
      )}
    </div>
  )
}
