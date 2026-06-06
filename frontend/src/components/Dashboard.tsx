import React from 'react'
import { Segment } from '../types'
import SegmentCard from './SegmentCard'
import { useCountUp } from '../utils'

export const OPEN_RATES: Record<string, number> = {
  vip: 0.52,
  lapsed: 0.18,
  first_timer: 0.38,
  high_spender: 0.45,
  local: 0.41,
  custom: 0.35,
}

interface Props {
  segments: Segment[]
  totalFans: number
  loading: boolean
  onGenerate: (segment: Segment) => void
}

const StatValue: React.FC<{ value: number; suffix?: string; prefix?: string }> = ({
  value,
  suffix = '',
  prefix = '',
}) => {
  const v = useCountUp(value)
  return (
    <div className="value mono">
      {prefix}
      {v.toLocaleString()}
      {suffix}
    </div>
  )
}

const Dashboard: React.FC<Props> = ({ segments, totalFans, loading, onGenerate }) => {
  const activeSegments = segments.filter((s) => s.count > 0)
  const projectedReach = segments.reduce((sum, s) => sum + s.count, 0)
  const avgOpen =
    activeSegments.length > 0
      ? activeSegments.reduce((sum, s) => sum + (OPEN_RATES[s.name] ?? 0.35), 0) /
        activeSegments.length
      : 0

  if (loading) {
    return (
      <div>
        <div className="statbar">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="stat">
              <div className="skeleton" style={{ height: 14, width: '60%' }} />
              <div className="skeleton" style={{ height: 28, width: '40%', marginTop: 10 }} />
            </div>
          ))}
        </div>
        <div className="seg-grid">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="seg-card">
              <div className="skeleton" style={{ height: 20, width: '50%' }} />
              <div className="skeleton" style={{ height: 44, width: '70%', margin: '12px 0' }} />
              <div className="skeleton" style={{ height: 14, width: '100%' }} />
              <div className="skeleton" style={{ height: 38, width: '100%', marginTop: 14 }} />
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (segments.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: 48 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>&#x1F41D;</div>
        <h2 style={{ marginBottom: 8 }}>No event loaded</h2>
        <p className="muted">Click “Load Demo Event” to ingest 500 fans and build segments.</p>
      </div>
    )
  }

  return (
    <div>
      <div className="statbar">
        <div className="stat">
          <div className="label">Total Fans</div>
          <StatValue value={totalFans} />
        </div>
        <div className="stat">
          <div className="label">Active Segments</div>
          <StatValue value={activeSegments.length} />
        </div>
        <div className="stat">
          <div className="label">Projected Reach</div>
          <StatValue value={projectedReach} />
        </div>
        <div className="stat">
          <div className="label">Avg Open Rate</div>
          <StatValue value={Math.round(avgOpen * 100)} suffix="%" />
        </div>
      </div>

      <div className="seg-grid">
        {segments.map((s) => (
          <SegmentCard
            key={s.name}
            segment={s}
            openRate={OPEN_RATES[s.name] ?? 0.35}
            onGenerate={onGenerate}
          />
        ))}
      </div>
    </div>
  )
}

export default Dashboard
