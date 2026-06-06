import React, { useState } from 'react'
import { ingestFixture, getSegments } from '../api'
import { Segment } from '../types'
import { DEMO_EVENTS } from '../demoEvents'

interface Props {
  event: { name: string; date: string; city: string; lat: number; lng: number }
  setEvent: (e: Props['event']) => void
  onSegments: (segs: Segment[], total: number) => void
  onLoadingChange: (loading: boolean) => void
  fanCount: number | null
  setFanCount: (n: number | null) => void
}

const EventIngestion: React.FC<Props> = ({
  event,
  setEvent,
  onSegments,
  onLoadingChange,
  fanCount,
  setFanCount,
}) => {
  const [rawJson, setRawJson] = useState('')
  const [error, setError] = useState('')

  const loadDemo = async () => {
    setError('')
    onLoadingChange(true)
    try {
      const res = await ingestFixture()
      setFanCount(res.data.fan_count)
      await refreshSegments()
    } catch (e) {
      setError('Could not reach backend on :5000')
    } finally {
      onLoadingChange(false)
    }
  }

  const refreshSegments = async () => {
    const res = await getSegments(event.lat, event.lng)
    const segs: Segment[] = Object.entries(res.data.segments).map(
      ([name, v]: [string, any]) => ({ name, count: v.count, fan_ids: v.fan_ids })
    )
    onSegments(segs, res.data.total_fans)
  }

  const set = (k: keyof Props['event'], v: string) => {
    const num = k === 'lat' || k === 'lng'
    setEvent({ ...event, [k]: num ? parseFloat(v) || 0 : v })
  }

  const pickDemo = (name: string) => {
    const d = DEMO_EVENTS.find((e) => e.name === name)
    if (d) setEvent({ name: d.name, date: d.date, city: d.city, lat: d.lat, lng: d.lng })
  }

  return (
    <div>
      <div className="panel-title">Event Ingestion</div>
      <div className="card">
        <div className="field">
          <label>Demo event</label>
          <select value={event.name} onChange={(e) => pickDemo(e.target.value)}>
            {DEMO_EVENTS.map((d) => (
              <option key={d.name} value={d.name}>
                {d.name} — {d.city} · {d.vibe}
              </option>
            ))}
          </select>
        </div>

        <button className="btn-primary" style={{ width: '100%' }} onClick={loadDemo}>
          Load Demo Event
        </button>

        {fanCount !== null && (
          <div style={{ marginTop: 12 }}>
            <span className="badge">&#10003; {fanCount} fans loaded</span>
          </div>
        )}
        {error && (
          <div style={{ marginTop: 12 }}>
            <span className="badge amber">{error}</span>
          </div>
        )}

        <div style={{ height: 1, background: 'var(--border)', margin: '16px 0' }} />

        <div className="field">
          <label>Event name</label>
          <input value={event.name} onChange={(e) => set('name', e.target.value)} />
        </div>
        <div className="field">
          <label>Event date</label>
          <input type="date" value={event.date} onChange={(e) => set('date', e.target.value)} />
        </div>
        <div className="field">
          <label>City</label>
          <input value={event.city} onChange={(e) => set('city', e.target.value)} />
        </div>
        <div className="row">
          <div className="field">
            <label>Lat</label>
            <input value={event.lat} onChange={(e) => set('lat', e.target.value)} />
          </div>
          <div className="field">
            <label>Lng</label>
            <input value={event.lng} onChange={(e) => set('lng', e.target.value)} />
          </div>
        </div>

        <details style={{ marginTop: 6 }}>
          <summary className="muted" style={{ cursor: 'pointer' }}>
            Paste raw fan JSON
          </summary>
          <textarea
            style={{ width: '100%', marginTop: 8, minHeight: 80 }}
            placeholder='{"fans":[...]}'
            value={rawJson}
            onChange={(e) => setRawJson(e.target.value)}
          />
        </details>
      </div>
    </div>
  )
}

export default EventIngestion
