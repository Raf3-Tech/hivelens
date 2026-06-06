import React, { useState } from 'react'
import { applyCustomFilter } from '../api'
import { CustomFilter, Segment } from '../types'

const GENRES = ['EDM', 'Hip Hop', 'Rock', 'Pop', 'Country', 'Jazz', 'Comedy']
const CITIES = ['Los Angeles', 'New York', 'Chicago', 'Toronto', 'Miami', 'Austin']
const WINDOWS: { label: string; value?: number }[] = [
  { label: '30d', value: 30 },
  { label: '90d', value: 90 },
  { label: '180d', value: 180 },
  { label: '1yr', value: 365 },
  { label: 'All', value: undefined },
]

interface Props {
  event: { lat: number; lng: number }
  onSave: (seg: Segment) => void
}

const SegmentBuilder: React.FC<Props> = ({ event, onSave }) => {
  const [genres, setGenres] = useState<string[]>([])
  const [cities, setCities] = useState<string[]>([])
  const [minSpend, setMinSpend] = useState(0)
  const [maxSpend, setMaxSpend] = useState(2000)
  const [minAttendance, setMinAttendance] = useState(0)
  const [windowIdx, setWindowIdx] = useState(4)
  const [activeOnly, setActiveOnly] = useState(true)
  const [radius, setRadius] = useState(100)
  const [count, setCount] = useState<number | null>(null)
  const [fanIds, setFanIds] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const toggle = (arr: string[], setArr: (v: string[]) => void, v: string) =>
    setArr(arr.includes(v) ? arr.filter((x) => x !== v) : [...arr, v])

  const buildFilters = (): CustomFilter => {
    const f: CustomFilter = {}
    if (genres.length) f.genres = genres
    if (cities.length) f.cities = cities
    if (minSpend > 0) f.min_spend_cents = minSpend * 100
    if (maxSpend < 2000) f.max_spend_cents = maxSpend * 100
    if (minAttendance > 0) f.min_attendance = minAttendance
    const w = WINDOWS[windowIdx].value
    if (w !== undefined) f.max_last_purchase_days = w
    if (activeOnly) f.email_status = 'active'
    if (radius < 100) {
      f.radius_miles = radius
      f.event_lat = event.lat
      f.event_lng = event.lng
    }
    return f
  }

  const apply = async () => {
    setLoading(true)
    try {
      const res = await applyCustomFilter(buildFilters())
      setCount(res.data.count)
      setFanIds(res.data.fan_ids)
    } finally {
      setLoading(false)
    }
  }

  const save = () => {
    if (count === null) return
    onSave({ name: 'custom', count, fan_ids: fanIds })
  }

  return (
    <div>
      <div className="panel-title">Build Custom Segment</div>
      <div className="card">
        <div className="field">
          <label>Genres (any of)</label>
          <div className="chips">
            {GENRES.map((g) => (
              <button
                key={g}
                className={`chip ${genres.includes(g) ? 'on' : ''}`}
                onClick={() => toggle(genres, setGenres, g)}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        <div className="field">
          <label>Cities</label>
          <div className="chips">
            {CITIES.map((c) => (
              <button
                key={c}
                className={`chip ${cities.includes(c) ? 'on' : ''}`}
                onClick={() => toggle(cities, setCities, c)}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        <div className="field">
          <label>
            Spend range: ${minSpend} &ndash; ${maxSpend}
          </label>
          <input
            type="range"
            min={0}
            max={2000}
            step={50}
            value={minSpend}
            onChange={(e) => setMinSpend(Math.min(+e.target.value, maxSpend))}
          />
          <input
            type="range"
            min={0}
            max={2000}
            step={50}
            value={maxSpend}
            onChange={(e) => setMaxSpend(Math.max(+e.target.value, minSpend))}
          />
        </div>

        <div className="field">
          <label>Min attendance: {minAttendance}</label>
          <input
            type="number"
            min={0}
            value={minAttendance}
            onChange={(e) => setMinAttendance(Math.max(0, +e.target.value))}
          />
        </div>

        <div className="field">
          <label>Last purchase within</label>
          <div className="chips">
            {WINDOWS.map((w, i) => (
              <button
                key={w.label}
                className={`chip ${windowIdx === i ? 'on' : ''}`}
                onClick={() => setWindowIdx(i)}
              >
                {w.label}
              </button>
            ))}
          </div>
        </div>

        <div className="field">
          <label>Email status</label>
          <div className="chips">
            <button
              className={`chip ${activeOnly ? 'on' : ''}`}
              onClick={() => setActiveOnly(true)}
            >
              Active only
            </button>
            <button
              className={`chip ${!activeOnly ? 'on' : ''}`}
              onClick={() => setActiveOnly(false)}
            >
              All
            </button>
          </div>
        </div>

        <div className="field">
          <label>Radius from event: {radius === 100 ? 'Any' : `${radius} mi`}</label>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={radius}
            onChange={(e) => setRadius(+e.target.value)}
          />
        </div>

        <button className="btn-secondary" style={{ width: '100%' }} onClick={apply} disabled={loading}>
          {loading ? 'Filtering…' : 'Apply Filters'}
        </button>

        {count !== null && (
          <div style={{ marginTop: 12, textAlign: 'center' }}>
            <span className="badge amber mono">{count.toLocaleString()} fans match</span>
            <button
              className="btn-primary"
              style={{ width: '100%', marginTop: 10 }}
              onClick={save}
              disabled={count === 0}
            >
              Save as Segment
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default SegmentBuilder
