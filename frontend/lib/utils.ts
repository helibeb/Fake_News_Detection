import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Helper function to format percentages
export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`
}

// Helper function to truncate text
export function truncateText(text: string, maxLength = 100): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + "..."
}

// Helper function to count words in text
export function countWords(text: string): number {
  return text.split(/\s+/).filter(Boolean).length
}

// Helper function to detect potentially problematic phrases
export function detectClickbaitPhrases(text: string): string[] {
  const clickbaitPhrases = [
    "you won't believe",
    "shocking",
    "mind-blowing",
    "this will shock you",
    "secret",
    "revealed",
    "amazing",
  ]

  const lowerText = text.toLowerCase()
  return clickbaitPhrases.filter((phrase) => lowerText.includes(phrase.toLowerCase()))
}
