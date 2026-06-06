import React, { useState } from 'react'
import EventIngestion from './components/EventIngestion'
import SegmentBuilder from './components/SegmentBuilder'
import Dashboard from './components/Dashboard'
import CampaignPreview from './components/CampaignPreview'
import { generateCampaign } from './api'
import { Campaign, Segment } from './types'

const DEFAULT_EVENT = {
  name: 'Rolling Loud LA 2026',
  date: '2026-08-15',
  city: 'Los Angeles',
  lat: 34.0522,
  lng: -118.2437,
}

const App: React.FC = () => {
  const [event, setEvent] = useState(DEFAULT_EVENT)
  const [fanCount, setFanCount] = useState<number | null>(null)
  const [segments, setSegments] = useState<Segment[]>([])
  const [totalFans, setTotalFans] = useState(0)
  const [loadingDash, setLoadingDash] = useState(false)

  const [drawerOpen, setDrawerOpen] = useState(false)
  const [campaignLoading, setCampaignLoading] = useState(false)
  const [campaign, setCampaign] = useState<Campaign | null>(null)
  const [activeSegment, setActiveSegment] = useState<Segment | null>(null)

  const handleSegments = (segs: Segment[], total: number) => {
    setSegments(segs)
    setTotalFans(total)
  }

  const runGenerate = async (segment: Segment) => {
    setActiveSegment(segment)
    setDrawerOpen(true)
    setCampaignLoading(true)
    setCampaign(null)
    try {
      const params: any = {
        segment: segment.name,
        event_name: event.name,
        event_date: event.date,
        event_city: event.city,
        event_lat: event.lat,
        event_lng: event.lng,
      }
      if (segment.name === 'custom') params.fan_ids = segment.fan_ids
      const res = await generateCampaign(params)
      setCampaign(res.data)
    } catch (e) {
      setCampaign(null)
    } finally {
      setCampaignLoading(false)
    }
  }

  const saveCustom = (seg: Segment) => {
    setSegments((prev) => {
      const without = prev.filter((s) => s.name !== 'custom')
      return [...without, seg]
    })
  }

  return (
    <div className="app">
      <div className="topbar">
        <span style={{ fontSize: 22 }}>&#x1F41D;</span>
        <span className="logo">
          Hive<span className="accent">Lens</span>
        </span>
        <span className="muted" style={{ marginLeft: 8 }}>
          Fan segmentation &amp; AI campaign studio
        </span>
      </div>

      <div className="sidebar">
        <EventIngestion
          event={event}
          setEvent={setEvent}
          onSegments={handleSegments}
          onLoadingChange={setLoadingDash}
          fanCount={fanCount}
          setFanCount={setFanCount}
        />
        <SegmentBuilder event={event} onSave={saveCustom} />
      </div>

      <div className="main">
        <Dashboard
          segments={segments}
          totalFans={totalFans}
          loading={loadingDash}
          onGenerate={runGenerate}
        />
      </div>

      <CampaignPreview
        open={drawerOpen}
        loading={campaignLoading}
        campaign={campaign}
        onClose={() => setDrawerOpen(false)}
        onRegenerate={() => activeSegment && runGenerate(activeSegment)}
      />
    </div>
  )
}

export default App
