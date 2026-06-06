import React from 'react'
import { BarChart, Bar, Cell, ResponsiveContainer, XAxis } from 'recharts'
import { Segment } from '../types'
import { segmentMeta, useCountUp } from '../utils'

interface Props {
  segment: Segment
  openRate: number
  onGenerate: (segment: Segment) => void
}

const SegmentCard: React.FC<Props> = ({ segment, openRate, onGenerate }) => {
  const meta = segmentMeta(segment.name)
  const count = useCountUp(segment.count)
  const ratePct = Math.round(openRate * 100)
  const data = [{ name: 'open', value: ratePct }]

  return (
    <div className="seg-card" style={{ borderLeftColor: meta.color }}>
      <div className="seg-head">
        <span className="seg-icon">{meta.icon}</span>
        <span className="seg-name">{meta.label}</span>
      </div>
      <div className="seg-count mono">{count.toLocaleString()}</div>
      <div className="seg-sub">fans in segment</div>

      <div className="openrate-label">
        <span>Projected open rate</span>
        <span className="mono" style={{ color: meta.color }}>
          {ratePct}%
        </span>
      </div>
      <div style={{ height: 14, marginBottom: 14 }}>
        <ResponsiveContainer width="100%" height={14}>
          <BarChart data={data} layout="vertical">
            <XAxis type="number" domain={[0, 100]} hide />
            <Bar dataKey="value" radius={4} background={{ fill: '#0f0f16' }}>
              <Cell fill={meta.color} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <button
        className="btn-secondary"
        style={{ width: '100%' }}
        disabled={segment.count === 0}
        onClick={() => onGenerate(segment)}
      >
        Generate Campaign
      </button>
    </div>
  )
}

export default SegmentCard
