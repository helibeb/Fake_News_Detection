import { NextResponse } from "next/server"

// This is a mock implementation for the frontend to work without the Python backend
// In a real application, this would forward the request to your Python backend

export async function POST(request) {
  try {
    const { text } = await request.json()

    if (!text || text.trim().length < 10) {
      return NextResponse.json({ error: "Text is too short for analysis" }, { status: 400 })
    }

    // Simulate processing time
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Simple heuristics for demonstration
    const lowerText = text.toLowerCase()
    const hasClickbait = /you won't believe|shocking|unbelievable|mind-blowing|secret|revealed/.test(lowerText)
    const hasExclamation = (text.match(/!/g) || []).length > 2
    const hasCredibleSources = /according to research|studies show|experts say|evidence suggests/.test(lowerText)

    // Calculate fake probability based on simple heuristics
    let fakeProbability = 0.5
    if (hasClickbait) fakeProbability += 0.2
    if (hasExclamation) fakeProbability += 0.1
    if (hasCredibleSources) fakeProbability -= 0.2

    // Clamp probability between 0.1 and 0.9
    fakeProbability = Math.max(0.1, Math.min(0.9, fakeProbability))

    // Determine prediction
    const prediction = fakeProbability > 0.5 ? "FAKE" : "REAL"
    const probability = prediction === "FAKE" ? fakeProbability : 1 - fakeProbability

    // Create feature contributions
    const emotionalContribution = hasClickbait ? 0.4 : 0.2
    const styleContribution = hasExclamation ? 0.3 : 0.1
    const sourceContribution = hasCredibleSources ? 0.4 : 0.2
    const statisticalContribution = 1 - (emotionalContribution + styleContribution + sourceContribution)

    // Normalize contributions to sum to 1
    const total = emotionalContribution + styleContribution + sourceContribution + statisticalContribution

    return NextResponse.json({
      prediction,
      probability,
      features: [
        {
          name: "Emotional Language",
          contribution: emotionalContribution / total,
          description: "High emotional content often indicates potential bias",
        },
        {
          name: "Writing Style",
          contribution: styleContribution / total,
          description: "Linguistic patterns common in misleading content",
        },
        {
          name: "Source Credibility",
          contribution: sourceContribution / total,
          description: "Analysis of cited sources and their reliability",
        },
        {
          name: "Statistical Consistency",
          contribution: statisticalContribution / total,
          description: "Evaluation of numerical claims and statistics",
        },
      ],
    })
  } catch (error) {
    console.error("Error analyzing text:", error)
    return NextResponse.json({ error: "Failed to analyze text" }, { status: 500 })
  }
}
