export interface DemoEvent {
  name: string
  date: string
  city: string
  lat: number
  lng: number
  vibe: string
}

/** Preset events the user can switch between in the demo. Different
 *  coordinates change the "local" segment counts, giving visible variety. */
export const DEMO_EVENTS: DemoEvent[] = [
  {
    name: 'Rolling Loud LA 2026',
    date: '2026-08-15',
    city: 'Los Angeles',
    lat: 34.0522,
    lng: -118.2437,
    vibe: 'Hip Hop',
  },
  {
    name: 'Electric Forest NYC',
    date: '2026-07-04',
    city: 'New York',
    lat: 40.7128,
    lng: -74.006,
    vibe: 'EDM',
  },
  {
    name: 'Lollapalooza Chicago',
    date: '2026-08-01',
    city: 'Chicago',
    lat: 41.8781,
    lng: -87.6298,
    vibe: 'Rock / Pop',
  },
  {
    name: 'Miami Bass Festival',
    date: '2026-12-31',
    city: 'Miami',
    lat: 25.7617,
    lng: -80.1918,
    vibe: 'EDM',
  },
  {
    name: 'Austin City Limits',
    date: '2026-10-03',
    city: 'Austin',
    lat: 30.2672,
    lng: -97.7431,
    vibe: 'Country / Rock',
  },
  {
    name: 'Toronto Jazz Nights',
    date: '2026-09-12',
    city: 'Toronto',
    lat: 43.6532,
    lng: -79.3832,
    vibe: 'Jazz',
  },
]
