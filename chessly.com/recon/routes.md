# Discovered Routes & Endpoints

> Extracted from Next.js build manifest (`_buildManifest.js`)

## Public Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/home` | Main dashboard (auth required) |
| `/home/beginners` | Beginner courses |
| `/home/legacy` | Legacy content |
| `/home/openings` | Opening courses |
| `/landing` | Landing page variant |
| `/join` | Join/signup page |
| `/plans` | Pricing plans |
| `/faqs` | FAQ page |
| `/contact` | Contact form |
| `/public/courses` | Public course listing |
| `/roadmap` | Development roadmap |

## Authentication

| Route | Description |
|-------|-------------|
| `/login` | Login page |
| `/register` | Registration page |
| `/authenticate` | OAuth/Stytch authentication callback |
| `/onboarding` | New user onboarding |
| `/password-reset` | Password reset |
| `/password-reset/email` | Password reset email form |
| `/password-reset/inbox-check` | Check inbox for reset email |
| `/link-discord` | Discord account linking |

## Courses & Learning

| Route | Description |
|-------|-------------|
| `/courses` | Course catalog |
| `/courses/[courseId]` | Individual course |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]` | Study within a chapter |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/video` | Video lesson |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/path-video` | Path video |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/quizzes` | Quiz |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/drill-shuffle` | Drill shuffle |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/lines` | Lines/analysis |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/analyze` | Analysis board |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/tiles/[tileIndex]` | Tile-based learning |
| `/courses/[courseId]/chapters/[chapterId]/studies/[studyId]/[variationId]/review` | Review variations |
| `/courses/[courseId]/review` | Course review |
| `/courses/[courseId]/drill-shuffle` | Drill shuffle for course |
| `/courses/[courseId]/drill-shuffle/setup` | Drill shuffle setup |
| `/courses/[courseId]/session/results` | Session results |
| `/drill-shuffle` | Global drill shuffle |
| `/non-opening-courses/[courseId]` | Non-opening courses |
| `/non-opening-courses/[courseId]/chapters/[chapterId]/lessons/[lessonId]` | Lessons |
| `/skill-courses/[courseId]` | Skill courses |
| `/skill-courses/[courseId]/chapters/[chapterId]/lessons/[lessonId]` | Skill lessons |
| `/skill-courses/[courseId]/chapters/[chapterId]/practice/[orderIndex]` | Practice |

## Chess AI

| Route | Description |
|-------|-------------|
| `/play-levi` | Chess AI "Levi" |
| `/play-levi/play` | Play against Levi |
| `/play-levi/game-review` | Review games |
| `/analyze` | Chess analysis board |

## Membership / Payments

| Route | Description |
|-------|-------------|
| `/membership` | Membership page |
| `/membership/[plan]` | Specific plan checkout |
| `/membership/[plan]/success` | Post-payment success |
| `/stripe-subscription-confirmation` | Stripe confirmation |
| `/stripe-subscription-cancelation` | Stripe cancellation |
| `/trials/success` | Trial success |
| `/course-owners-discount` | Discount for course owners |
| `/courseowners` | Course owner area |

## User / Social

| Route | Description |
|-------|-------------|
| `/profiles` | User profiles listing |
| `/profiles/[username]` | Individual user profile |
| `/leaderboards` | XP leaderboard |
| `/settings` | User settings |
| `/settings/board-customization` | Board customization |
| `/settings/change-email-address` | Change email flow |
| `/settings/confirm-current-email` | Confirm current email |
| `/settings/confirm-new-email` | Confirm new email |
| `/settings/email-change-success` | Email change success |
| `/settings/reset-progress` | Reset progress |

## Pawn Shop (Gamification)

| Route | Description |
|-------|-------------|
| `/pawn-shop` | Pawn shop |
| `/pawn-shop/videos/[videoId]` | Pawn shop videos |
| `/pawn-shop/gte-reward` | Guess The Elo reward |
| `/pawn-shop/guess-the-elo/submit` | GTE submission |
| `/pawn-shop/hoodie-video` | Hoodie video |
| `/pawn-shop/raffles/hidden-hoodie-video` | Hidden hoodie raffle |

## Legal

| Route | Description |
|-------|-------------|
| `/terms-of-use` | Terms of Service |
| `/privacy-policy` | Privacy Policy |
| `/cookie-policy` | Cookie Policy |

## Other

| Route | Description |
|-------|-------------|
| `/404` | Custom 404 page |
| `/delete-account` | Account deletion |
| `/embed/[vimeoVideoId]` | Vimeo video embedding |
| `/events/holiday` | Holiday event |
| `/events/valentines` | Valentine's event |
| `/no-access` | No access page |
| `/viponly` | VIP-only content |
