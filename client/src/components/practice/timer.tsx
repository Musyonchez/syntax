"use client"

import { useState, useEffect, useCallback } from 'react'
import { Clock } from 'lucide-react'

interface TimerProps {
  isActive: boolean
  maxTime: number
  onTimeUpdate: (time: number) => void
  initialTime?: number
  className?: string
}

export function Timer({ 
  isActive, 
  maxTime, 
  onTimeUpdate, 
  initialTime = 0,
  className = ""
}: TimerProps) {
  const [time, setTime] = useState(initialTime)

  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null

    if (isActive && time < maxTime) {
      intervalId = setInterval(() => {
        setTime(prevTime => {
          const newTime = prevTime + 1
          onTimeUpdate(newTime)
          return newTime
        })
      }, 1000)
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    }
  }, [isActive, time, maxTime, onTimeUpdate])

  // Reset time when initialTime changes
  useEffect(() => {
    setTime(initialTime)
  }, [initialTime])

  const formatTime = useCallback((seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }, [])

  const getTimeColor = useCallback(() => {
    const ratio = time / maxTime
    if (ratio < 0.5) return 'text-green-600'
    if (ratio < 0.8) return 'text-yellow-600'
    return 'text-red-600'
  }, [time, maxTime])

  const isOvertime = time >= maxTime

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <Clock className={`w-4 h-4 ${getTimeColor()}`} />
      <span className={`font-mono ${getTimeColor()} ${isOvertime ? 'animate-pulse' : ''}`}>
        {formatTime(time)}
        {isOvertime && ' (OVERTIME)'}
      </span>
    </div>
  )
}