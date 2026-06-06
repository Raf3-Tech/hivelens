import { useEffect, useState } from 'react'

export function formatCurrency(cents: number): string {
  return (cents / 100).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

export const SEGMENT_META: Record<string, { icon: string; color: string; label: string }> = {
  vip: { icon: '\u{1F451}', color: '#f5a623', label: 'VIP' },
  lapsed: { icon: '\u{23F1}', color: '#ff5a5f', label: 'Lapsed' },
  first_timer: { icon: '\u{2B50}', color: '#00b4a6', label: 'First Timer' },
  high_spender: { icon: '\u{1F48E}', color: '#a06bff', label: 'High Spender' },
  local: { icon: '\u{1F4CD}', color: '#4fa6ff', label: 'Local' },
}

export function segmentMeta(name: string) {
  return (
    SEGMENT_META[name] || {
      icon: '\u{1F3AF}',
      color: '#f5a623',
      label: name.replace(/_/g, ' '),
    }
  )
}

/** Animate a number from 0 up to `target` over `duration` ms. */
export function useCountUp(target: number, duration = 900): number {
  const [value, setValue] = useState(0)
  useEffect(() => {
    let raf = 0
    const start = performance.now()
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration)
      // easeOutCubic
      const eased = 1 - Math.pow(1 - t, 3)
      setValue(Math.round(target * eased))
      if (t < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [target, duration])
  return value
}
