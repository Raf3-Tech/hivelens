import axios from 'axios'
import { CustomFilter } from './types'

const BASE = 'http://localhost:5000/api'

export const ingestFixture = () => axios.post(`${BASE}/ingest`, { use_fixture: true })

export const getSegments = (lat: number, lng: number) =>
  axios.post(`${BASE}/segments`, { event_lat: lat, event_lng: lng })

export const applyCustomFilter = (filters: CustomFilter) =>
  axios.post(`${BASE}/segment/custom`, { filters })

export const generateCampaign = (params: object) =>
  axios.post(`${BASE}/campaign/generate`, params)

export const getFanSample = (segment: string, limit = 5) =>
  axios.get(`${BASE}/fans/sample?segment=${segment}&limit=${limit}`)
