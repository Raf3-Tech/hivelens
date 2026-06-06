"""Hand-written campaign copy used when no Claude API key is available.

Each segment has multiple distinct variants so that regenerating a campaign
produces fresh-feeling copy, mimicking a live Claude-powered experience.

Tokens replaced at render time:
  __EVENT__  -> event name
  __DATE__   -> event date
  __CITY__   -> event city
The literal "{first_name}" placeholder is preserved for downstream mail-merge.
SMS bodies keep the "[link]" placeholder.
"""

def render(text: str, event_name: str, event_date: str, event_city: str) -> str:
    """Substitute event tokens, preserving {first_name} and [link] placeholders."""
    city = event_city or "your city"
    return (text.replace("__EVENT__", event_name)
                .replace("__DATE__", event_date)
                .replace("__CITY__", city))


FALLBACK_TEMPLATES = {
    "vip": [
        {
            "subject": "__EVENT__: your VIP doors open first",
            "email": (
                "Hi {first_name},\n\n"
                "You've been with us through the loudest nights, and __EVENT__ on "
                "__DATE__ deserves the same treatment you've earned. Before a single "
                "public ticket drops, your VIP presale is unlocked — first pick of "
                "seats, the shortest line, and entry to the members lounge where the "
                "first round is on us.\n\n"
                "This year we rebuilt the production from the ground up: a wider stage, "
                "a deeper sound system, and an after-set session reserved for our top "
                "fans only. We saved you a spot near the front, but VIP allocation is "
                "capped and the best upgrades move within hours of going live.\n\n"
                "Claim your VIP access now, bring someone who'll get it, and let's make "
                "__CITY__ remember this one.\n\n"
                "Doors open early for you,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, your __EVENT__ VIP presale is live — first seats, "
                "lounge access, early doors. Claim before it caps: [link]"
            ),
        },
        {
            "subject": "Your loyalty unlocks __EVENT__ early",
            "email": (
                "Hi {first_name},\n\n"
                "Loyalty like yours doesn't go unnoticed. Because you're one of our "
                "most dedicated fans, you're getting __EVENT__ before everyone else — a "
                "private presale window for __DATE__ that opens today.\n\n"
                "Here's what your VIP tier includes this year: early entry, premium "
                "viewing decks, a dedicated bar with no wait, and an exclusive backstage "
                "meet reserved for a handful of guests. We held these back specifically "
                "for fans who show up season after season.\n\n"
                "Tickets for the general public go live next week, and the upgrades you "
                "actually want tend to vanish fast. Lock yours in while the full menu is "
                "still open. We can't wait to welcome you back to the front of the room "
                "in __CITY__ for a night built around the fans who never miss one.\n\n"
                "With gratitude,\nThe __EVENT__ Crew"
            ),
            "sms": (
                "{first_name}, VIP early access to __EVENT__ is open now — premium "
                "decks, no-wait bar, backstage meet. Reserve yours: [link]"
            ),
        },
        {
            "subject": "__EVENT__ VIP: backstage is calling",
            "email": (
                "Hi {first_name},\n\n"
                "Some nights are worth clearing your calendar for — __EVENT__ on "
                "__DATE__ is one of them, and your VIP invitation is officially open.\n\n"
                "You've spent enough nights up front to know the difference good access "
                "makes. This year we leaned all the way in: skip-the-line entry, an "
                "elevated viewing platform with the best sightlines in the house, "
                "complimentary drinks in the VIP lounge, and a limited backstage "
                "experience for our most loyal crowd.\n\n"
                "We're holding your place, but VIP is intentionally small. Once these "
                "upgrades are claimed, they're gone — no waitlist, no encore. Grab your "
                "spot, tell a friend who deserves the full treatment, and we'll see you "
                "in __CITY__.\n\n"
                "Save the date,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, your __EVENT__ VIP invite is live — skip-the-line entry, "
                "lounge drinks, backstage access. Claim it before it's gone: [link]"
            ),
        },
        {
            "subject": "__EVENT__ presale: your name's on the list",
            "email": (
                "Hi {first_name},\n\n"
                "The list is short, and you're on it. __EVENT__ returns on __DATE__, and "
                "before the general public hears a word, your VIP presale is "
                "unlocked.\n\n"
                "You already know the difference real access makes — that's why we held "
                "back the good stuff for fans like you. This year that means "
                "front-of-house viewing, a private lounge with complimentary drinks, "
                "express entry that skips the crowd entirely, and a limited backstage "
                "moment reserved for our most loyal names.\n\n"
                "We're holding your place, but VIP runs lean by design. Once the upgrades "
                "are claimed, that's it — no second release. Secure yours, bring someone "
                "worthy of the full experience, and we'll roll out the carpet in "
                "__CITY__.\n\n"
                "First in line, always,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, you're on the __EVENT__ VIP list — express entry, private "
                "lounge, backstage moment. Claim before it closes: [link]"
            ),
        },
        {
            "subject": "Before anyone else: __EVENT__ VIP",
            "email": (
                "Hi {first_name},\n\n"
                "Consider this your head start. __EVENT__ takes over __CITY__ on __DATE__, "
                "and your VIP access is open a full week before tickets reach everyone "
                "else.\n\n"
                "Loyalty earns more than a thank-you here. Your tier unlocks the best "
                "sightlines in the building, a members-only bar with zero wait, early "
                "entry while the venue is still calm, and an exclusive backstage "
                "experience we don't advertise. It's the version of the night most "
                "people never get to see.\n\n"
                "These spots are deliberately few, and they tend to disappear the moment "
                "word gets out. Lock yours in now, while the full lineup of perks is still "
                "on the table and the best of the night is still yours to claim.\n\n"
                "We'll see you out front,\nThe __EVENT__ Crew"
            ),
            "sms": (
                "{first_name}, your week-early __EVENT__ VIP access is open — best views, "
                "no-wait bar, backstage. Grab it first: [link]"
            ),
        },
    ],
    "lapsed": [
        {
            "subject": "We saved you a spot at __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "It's been a while, and honestly, the crowd hasn't felt the same without "
                "you. __EVENT__ is back in __CITY__ on __DATE__, and we wanted you to be "
                "among the first to know.\n\n"
                "A lot has changed since your last night with us — a reimagined lineup, "
                "new headliners we think you'll love, and a venue upgrade that finally "
                "fixes the things you told us about. To make the trip back easy, here's "
                "20% off your return ticket with code WELCOME20.\n\n"
                "No pressure, no catch. Just an open door and a night that might remind "
                "you why you started coming in the first place. Come back and pick up "
                "right where you left off.\n\n"
                "We've missed you,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, we miss you. __EVENT__ returns to __CITY__ __DATE__ — "
                "here's 20% off with WELCOME20. Come back: [link]"
            ),
        },
        {
            "subject": "Your comeback ticket to __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "Life gets busy — we get it. But __EVENT__ on __DATE__ felt like the "
                "right reason to reach out, because some of our best memories had you in "
                "the crowd.\n\n"
                "We've been busy too. The new lineup is the strongest we've booked in "
                "years, the sound system finally got the overhaul it needed, and we "
                "added the late-night sets people kept asking for. We'd love for you to "
                "see it firsthand.\n\n"
                "To welcome you back, your next ticket is 25% off — just use COMEBACK25 "
                "at checkout. It's our way of saying the door's still open. Round up the "
                "crew or come solo. Either way, __CITY__ won't be the same until you're "
                "back in it.\n\n"
                "Hope to see you soon,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, it's been too long. __EVENT__ hits __CITY__ __DATE__ — "
                "25% off your return with COMEBACK25. Save your spot: [link]"
            ),
        },
        {
            "subject": "A reason to come back to __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "We noticed you haven't joined us in a while, and we'd hate for you to "
                "miss what's coming. __EVENT__ lands in __CITY__ on __DATE__, and it's "
                "shaping up to be one to remember.\n\n"
                "Think bigger names, a refreshed stage design, and the kind of energy "
                "that made you a fan in the first place. We've listened to what our "
                "community wanted and built this one around it.\n\n"
                "As a returning fan, you've got early access plus a 20% loyalty discount "
                "waiting — code RETURN20. No strings, just a warm welcome back to the "
                "front row. Give us one more night. We have a feeling it'll be worth "
                "it.\n\n"
                "See you back in the crowd,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, your seat at __EVENT__ in __CITY__ on __DATE__ is waiting "
                "— 20% off with RETURN20. Back to the front row: [link]"
            ),
        },
        {
            "subject": "Your BACK20 code for __EVENT__ is waiting",
            "email": (
                "Hi {first_name},\n\n"
                "It has been too long since we last saw you in __CITY__, and the room hasn't felt quite the same without you.\n\n"
                "We have been putting together something special for __EVENT__ on __DATE__, and the lineup this year is the strongest we have ever booked. New headliners, fresh sounds, and the same energy you remember from the nights you used to love.\n\n"
                "Because we genuinely miss having you in the crowd, here is a thank-you just for you: use code BACK20 at checkout for twenty percent off any ticket. Think of it as our way of saving you a seat and welcoming you home.\n\n"
                "The doors of __CITY__ are open again, {first_name}, and there is a place waiting for you on the floor. Come back and dance with us.\n\n"
                "We promise it will feel exactly like you remembered, only louder."
            ),
            "sms": (
                "Hi {first_name}, we miss you! __EVENT__ hits __CITY__ on __DATE__. New "
                "lineup, and BACK20 gets you 20% off. Come home: [link]"
            ),
        },
        {
            "subject": "WELCOME25: a fresh start at __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "A lot has changed since your last night out with us, and we think you are going to love where things are headed.\n\n"
                "For __EVENT__ on __DATE__, we rebuilt the whole experience around the artists you have been streaming all year. The new lineup just dropped, and it reads like a playlist made specifically for you.\n\n"
                "We never forgot the way you showed up for the music, so we want to make your return easy. Use code WELCOME25 for twenty-five percent off your ticket, our way of clearing the path back to __CITY__.\n\n"
                "No pressure and no catch, {first_name}, just an open invitation to pick up exactly where you left off.\n\n"
                "Grab your spot, turn the volume up, and let us remind you why you fell for live music in the first place."
            ),
            "sms": (
                "{first_name}, the new __EVENT__ lineup is live! Back in __CITY__ on "
                "__DATE__. WELCOME25 = 25% off your return ticket. See it: [link]"
            ),
        },
    ],
    "first_timer": [
        {
            "subject": "Welcome to __EVENT__ — what to expect",
            "email": (
                "Hi {first_name},\n\n"
                "Welcome to the family — we're genuinely excited you're joining us for "
                "__EVENT__ on __DATE__. Since it's your first time, here's everything "
                "you need to walk in like a regular.\n\n"
                "Doors open early, so arrive with time to explore the __CITY__ venue, "
                "grab food, and stake out your favorite spot before the headliners hit. "
                "Comfortable shoes are non-negotiable, a portable charger is a "
                "lifesaver, and the official app has the full set times so you never "
                "miss a moment.\n\n"
                "The crowd here looks out for each other — say hi to the people around "
                "you, and you'll leave with new friends and a story or two. Any "
                "questions before the big night? Just reply. We've got you.\n\n"
                "See you up front,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, welcome to __EVENT__! First time? Arrive early, charge "
                "up, grab the app for set times. See you __DATE__: [link]"
            ),
        },
        {
            "subject": "Your first __EVENT__ — insider guide",
            "email": (
                "Hi {first_name},\n\n"
                "First show with us? You picked a great one. __EVENT__ on __DATE__ is "
                "the kind of night people talk about for years, and we want yours to be "
                "unforgettable from the moment you arrive.\n\n"
                "A few insider tips: get to the __CITY__ venue early to beat the lines, "
                "travel light because security is quicker that way, and download the "
                "event app to map out which sets you can't miss. Hydrate, pace yourself, "
                "and don't be shy — some of the best moments happen between songs with "
                "the people next to you.\n\n"
                "Thousands of fans came through last season and called it their "
                "highlight of the year. Now it's your turn. We'll be looking for you in "
                "the crowd.\n\n"
                "Welcome aboard,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, your first __EVENT__ is almost here! Arrive early, pack "
                "light, grab the app. See you __DATE__ in __CITY__: [link]"
            ),
        },
        {
            "subject": "Everything you need for __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "You're in — and your first __EVENT__ is going to be a night to "
                "remember. Happening __DATE__ in __CITY__, this is where new fans become "
                "lifers, and we want your debut to be seamless.\n\n"
                "Here's the short version: arrive early to soak in the atmosphere, wear "
                "something you can dance in, and keep your phone charged for the moments "
                "you'll want to relive. The official app has set times, maps, and entry "
                "tips, so you'll always know where to be.\n\n"
                "Most first-timers tell us the same thing afterward — they wish they'd "
                "come sooner. Once you feel that first drop with the whole crowd, you'll "
                "understand why. Can't wait to welcome you in person.\n\n"
                "See you soon,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, welcome to __EVENT__! Your first show is __DATE__ in "
                "__CITY__ — arrive early, charge up, check the app: [link]"
            ),
        },
        {
            "subject": "First time at __EVENT__? Read this",
            "email": (
                "Hi {first_name},\n\n"
                "You're heading to your first __EVENT__, and we want you walking in like you've done this a hundred times. Here's the insider rundown.\n\n"
                "Arrive early. Gates in __CITY__ fill fast, and the opening sets are often the ones people talk about for months. Getting in ahead of the rush means more music and less waiting.\n\n"
                "Travel light. A small bag clears security quicker, and your shoulders will thank you by hour three. Charge your phone before you leave, then download the event app. It maps every stage and pushes set times so you never miss the artist you came for.\n\n"
                "Last year, thousands of first-timers told us they left already planning their return. We saved you a spot on __DATE__.\n\n"
                "Come ready, and we'll take care of the rest.\n\nSee you there,\nThe __EVENT__ Team"
            ),
            "sms": (
                "Hi {first_name}! First __EVENT__? Arrive early, pack light, charge up, "
                "grab the app for set times. First-timer guide: [link]"
            ),
        },
        {
            "subject": "Your __EVENT__ game plan starts here",
            "email": (
                "Hi {first_name},\n\n"
                "Your first __EVENT__ is almost here, and a little prep turns a good night into one you'll remember. Consider this your game plan.\n\n"
                "Get to __CITY__ early. The lines are shortest before doors, and early sets often become the weekend's biggest surprises.\n\n"
                "Pack light. One small bag means you breeze through security and stay free to move between stages all day. Charge your phone fully, then open the event app. It holds the full map and live set times, so you'll always know where your favorite artist plays next.\n\n"
                "More than ninety percent of first-timers from last season came back for another show. Once you feel the room, you'll understand why.\n\n"
                "Mark __DATE__, follow these tips, and arrive ready to make it yours.\n\nWelcome to the family,\nThe __EVENT__ Team"
            ),
            "sms": (
                "Hi {first_name}! New to __EVENT__? Game plan: come early, travel light, "
                "charge up, use the app for set times. Tips here: [link]"
            ),
        },
    ],
    "high_spender": [
        {
            "subject": "An upgrade worthy of __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "You appreciate the finer details, so we'll get straight to it: "
                "__EVENT__ on __DATE__ has a premium tier built for guests exactly like "
                "you.\n\n"
                "Picture skipping every line, settling into a private VIP lounge with "
                "bottle service, watching from an elevated deck with unobstructed "
                "sightlines, and rounding out the night with a meet-and-greet most fans "
                "only dream about. Add premium parking steps from the entrance, and the "
                "entire evening runs effortlessly.\n\n"
                "These experiences are deliberately limited — a small number of guests, "
                "a much bigger night. We're extending first access to you before they "
                "open more widely. Treat yourself to the version of __EVENT__ you "
                "deserve, and arrive in __CITY__ ready for something elevated.\n\n"
                "To the finer things,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, elevate your __EVENT__ night — VIP lounge, premium "
                "parking, meet & greet. Limited upgrades open now: [link]"
            ),
        },
        {
            "subject": "__EVENT__: the premium experience is open",
            "email": (
                "Hi {first_name},\n\n"
                "For guests who expect more, __EVENT__ on __DATE__ delivers. We've put "
                "together a premium package that turns a great show into a flawless "
                "evening.\n\n"
                "Your upgrade includes a dedicated entrance with zero wait, an exclusive "
                "lounge with full bar and chef-prepared bites, prime elevated viewing, "
                "and a meet-and-greet with talent before the headline set. Premium valet "
                "parking means you arrive and leave on your terms — no hassle, no "
                "crowds.\n\n"
                "We're offering this to our highest-value guests first, ahead of the "
                "general upgrade release. Allocation is intentionally small to keep the "
                "experience exclusive. Step into the best seat in __CITY__, and all you "
                "have to do is show up — we'll handle every detail.\n\n"
                "At your service,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, your premium __EVENT__ upgrade is ready — valet parking, "
                "private lounge, artist meet & greet. Reserve early: [link]"
            ),
        },
        {
            "subject": "Reserved for you: __EVENT__ VIP add-ons",
            "email": (
                "Hi {first_name},\n\n"
                "Some nights call for the full experience, and __EVENT__ on __DATE__ is "
                "one of them. Because you invest in the moments that matter, we're "
                "inviting you to upgrade before anyone else.\n\n"
                "Your premium options this year: a members-only lounge with "
                "complimentary bar, an elevated platform with the cleanest view in the "
                "house, a backstage meet-and-greet, and reserved parking just steps from "
                "the gate. Every detail is designed so you spend the night enjoying the "
                "show, not waiting in line.\n\n"
                "We keep these experiences small on purpose, which means they go "
                "quickly. Securing yours early guarantees the tier you actually want. "
                "Come to __CITY__ and experience __EVENT__ the way it's meant to be "
                "seen.\n\n"
                "Cheers,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, upgrade your __EVENT__ night — lounge access, best views, "
                "backstage meet, reserved parking. Claim early: [link]"
            ),
        },
        {
            "subject": "Your front-row chapter of __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "You already know what a great night feels like. For __EVENT__ in __CITY__, we want yours to be unforgettable from the first note.\n\n"
                "A limited block of elevated viewing decks just opened. Picture watching the headliners from a private balcony, drink in hand, with bottle service brought straight to your table and no lines between you and the music.\n\n"
                "If you would rather be closer to the artists, a small number of meet and greet passes are still available. Step backstage, share a moment, and leave with more than a ticket stub.\n\n"
                "These add-ons sit alongside your existing seats, so upgrading takes two minutes. On __DATE__, the difference between a good night and a legendary one is one decision.\n\n"
                "Reply or tap below to reserve before this block sells through.\n\nSee you in __CITY__,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, decks & meet-greet passes for __EVENT__ on __DATE__ just "
                "opened. Reserve yours before they sell out: [link]"
            ),
        },
        {
            "subject": "__EVENT__: step into the VIP lounge",
            "email": (
                "Hi {first_name},\n\n"
                "Some nights deserve more than a seat. For __EVENT__ in __CITY__, we are opening the doors to a side of the show most guests never see.\n\n"
                "VIP lounge access means a private bar, comfortable space away from the crowd, and a fast track in and out of the venue. Pair it with premium valet parking and your evening begins the moment you arrive, not after the walk from the lot.\n\n"
                "Want the full treatment? Add a meet and greet and watch the show from our reserved deck with bottle service on hand all night.\n\n"
                "Your current tickets stay exactly as they are. These upgrades simply elevate everything around them, and the lounge has limited capacity.\n\n"
                "Secure your spot for __DATE__ while places remain.\n\nWith you in __CITY__,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, VIP lounge + valet for __EVENT__ on __DATE__ is now open, "
                "limited spots. Claim yours here: [link]"
            ),
        },
    ],
    "local": [
        {
            "subject": "__EVENT__ is happening in __CITY__",
            "email": (
                "Hi {first_name},\n\n"
                "Big news for the home crowd: __EVENT__ is happening right here in "
                "__CITY__ on __DATE__, practically in your backyard. No flights, no "
                "hotels — just a short trip to one of the biggest nights of the "
                "season.\n\n"
                "Since you're local, you've got the home-field advantage. Skip the "
                "travel stress, roll in day-of, and grab a friend on the way — our "
                "bring-a-buddy deal means two tickets for less when you book together. "
                "Knowing the area, you already have the parking and shortcuts figured "
                "out.\n\n"
                "Tickets are moving fast as the date gets closer, and local demand is "
                "real. Lock yours in before your city sells out from under you. Your "
                "scene, your night — let's go.\n\n"
                "See you down the street,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, __EVENT__ is right here in __CITY__ on __DATE__! No "
                "travel — grab a friend with our bring-a-buddy deal: [link]"
            ),
        },
        {
            "subject": "Right around the corner: __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "The wait is over for __CITY__ — __EVENT__ lands in your city on "
                "__DATE__, and being local has never paid off more.\n\n"
                "While everyone else books flights and hotels, you're a short ride away. "
                "Show up day-of, beat the out-of-towners to the best spots, and make a "
                "night of it without ever leaving home. Bring someone along with our "
                "two-for-one local deal, and the night gets even better.\n\n"
                "Here's the catch: hometown shows sell fast, and the closer we get, the "
                "thinner availability gets. We'd hate for you to miss the one event "
                "happening in your own backyard. Claim your tickets now and own the "
                "night that's right outside your door.\n\n"
                "See you in the crowd,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, __EVENT__ comes to __CITY__ on __DATE__! Skip the travel, "
                "bring a friend two-for-one, own your hometown night: [link]"
            ),
        },
        {
            "subject": "Your city, your night: __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "__CITY__, this one's for you. __EVENT__ is coming to your city on "
                "__DATE__, and as a local, you're first to hear about it.\n\n"
                "No airfare, no overnight bags — just a quick trip to a night you'll be "
                "talking about for weeks. Come straight from work or make a whole day of "
                "it; either way, the home crowd always brings the best energy. Bundle "
                "tickets with a friend and our local bring-a-buddy offer makes it an "
                "easy yes.\n\n"
                "Demand from the neighborhood is climbing fast, and day-of tickets won't "
                "stick around. Grab yours now so you're guaranteed a spot when __EVENT__ "
                "takes over __CITY__. Let's show them how we do it at home.\n\n"
                "See you soon,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, __EVENT__ takes over __CITY__ on __DATE__! No travel, "
                "bring a buddy, day-of convenience. Lock in your night: [link]"
            ),
        },
        {
            "subject": "__EVENT__ is in your backyard, {first_name}",
            "email": (
                "Hi {first_name},\n\n"
                "No flights, no hotel, no long drive. __EVENT__ is landing right here in __CITY__ on __DATE__, which means the best night of the season is a short walk or quick ride away.\n\n"
                "You know these streets better than anyone, so use that hometown advantage. Roll up day-of, skip the travel stress, and be in the crowd while everyone else is still checking maps.\n\n"
                "We saved a batch of last-minute tickets for fans close by, and they tend to disappear fast once word gets around the neighborhood.\n\n"
                "Here is the move: grab two. Bring a friend, a neighbor, or whoever owes you a great night out. The room sounds better when your people are in it with you.\n\n"
                "This is your city and your night. Claim your spot before __CITY__ fills the room without you.\n\nSee you there,\nThe __EVENT__ Crew"
            ),
            "sms": (
                "{first_name}, __EVENT__ hits __CITY__ on __DATE__. No travel needed. "
                "Grab last-minute tickets, bring a friend: [link]"
            ),
        },
        {
            "subject": "Skip the drive, {first_name} — __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "Some nights you have to travel for. This is not one of them. __EVENT__ comes to __CITY__ on __DATE__, so the only commute you need is the one to your own front door and back.\n\n"
                "That is the hometown perk. While out-of-towners book rooms and map out parking, you can leave late, stay as long as you want, and sleep in your own bed after.\n\n"
                "We are holding a final wave of tickets for fans nearby, and they are moving quickly. Lock yours in now so the night does not slip past you.\n\n"
                "Even better, make it two. Our bring-a-friend deal lets you split the fun and double the energy for the same easy trip across town.\n\n"
                "__CITY__ rarely gets a night like this. Grab your tickets and own it.\n\nSee you soon,\nThe __EVENT__ Crew"
            ),
            "sms": (
                "{first_name}, no hotel, no hassle. __EVENT__ in __CITY__ on __DATE__. "
                "Last-minute two-for-one tickets here: [link]"
            ),
        },
    ],
    "_default": [
        {
            "subject": "__EVENT__ — your invitation is here",
            "email": (
                "Hi {first_name},\n\n"
                "We put this one together with you in mind. __EVENT__ is happening in "
                "__CITY__ on __DATE__, and based on what you love, we think it's right "
                "up your alley.\n\n"
                "Expect a lineup tuned to your taste, an atmosphere built for the people "
                "who actually show up, and a few surprises we're keeping under wraps for "
                "now. Whether you come for the headliners or the whole experience, "
                "there's a spot here with your name on it.\n\n"
                "Tickets are available now, and the best ones tend to go early. Secure "
                "yours while the full range is still open, and bring someone who'd "
                "appreciate a night like this. We'd love to see you there.\n\n"
                "Until then,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, __EVENT__ is coming to __CITY__ on __DATE__ — handpicked "
                "for fans like you. Grab your tickets early: [link]"
            ),
        },
        {
            "subject": "Something you'll want to see: __EVENT__",
            "email": (
                "Hi {first_name},\n\n"
                "This is the kind of night that doesn't come around often. __EVENT__ "
                "takes the stage in __CITY__ on __DATE__, and we wanted to make sure it "
                "landed on your radar.\n\n"
                "We've shaped every detail — the lineup, the production, the energy — "
                "around fans who know a good show when they see one. Come for a few "
                "hours of escape, a soundtrack you'll be humming for days, and a crowd "
                "that knows how to make a night count. No matter how you like to "
                "experience a show, there's room for you here.\n\n"
                "Availability is open now, but the prime spots rarely last. Reserve "
                "yours early, round up your people, and let's make __DATE__ one to "
                "remember.\n\n"
                "Cheers,\nThe __EVENT__ Team"
            ),
            "sms": (
                "{first_name}, __EVENT__ takes the stage in __CITY__ on __DATE__. Prime "
                "spots go fast — reserve yours now: [link]"
            ),
        },
        {
            "subject": "__EVENT__ tickets are moving fast",
            "email": (
                "Hi {first_name},\n\n"
                "We built __EVENT__ around the kind of lineup you actually want to hear, and now it is almost here. The show takes over __CITY__ on __DATE__, and we wanted you to have first word.\n\n"
                "This one is shaping up around sounds and artists that match your taste, so it should feel less like a random night out and more like a setlist made for you.\n\n"
                "Availability is limited. Tickets are already moving, and the best seats in the house go to the people who act first rather than wait until the week of the show.\n\n"
                "Consider this your open invitation. Whether you come solo or pull together a crew, there is a spot here with your name on it.\n\n"
                "Pick your tickets now and we will see you when the lights drop in __CITY__.\n\nUntil then,\nThe __EVENT__ Crew"
            ),
            "sms": (
                "{first_name}, __EVENT__ hits __CITY__ on __DATE__. A lineup tuned to your "
                "taste, limited tickets. Claim yours: [link]"
            ),
        },
    ],
}
