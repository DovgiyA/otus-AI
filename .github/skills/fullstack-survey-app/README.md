# Full-Stack Survey App Skill

This skill (`fullstack-survey-app`) provides a **complete, tested methodology** for building minimal full-stack survey/form applications.

## What You Get

✅ **Fully functional app** in 2-3 hours:
- Backend API (FastAPI) with persistence
- Frontend UI (React + MobX)
- SQLite database (auto-created)
- Comprehensive documentation
- All development prompts archived

✅ **Verified workflow** covering:
- Architecture planning
- Backend implementation (models, schemas, routes)
- Frontend implementation (components, store, styling)
- Integration testing
- Complete documentation

✅ **Quality gates** at each phase:
- Backend tests
- Frontend tests
- End-to-end tests
- Database verification

## When to Use

**Perfect for:**
- Surveys with 3-10 questions
- Questionnaires (feedback, satisfaction, research)
- Form applications with backend storage
- MVP/POC data collection tools
- Learning full-stack development

**Not ideal for:**
- Websites (use web frameworks)
- AI applications (use specialized tools)
- Real-time collaborative apps (need WebSocket)
- Complex business logic (scale up architecture)

## Quick Start

1. **Read** `SKILL.md` to understand the 5-phase methodology
2. **Review** `architecture.md` for system design
3. **Check** `../prompts/` for reusable prompt templates
4. **Follow** the checklist in Phase 1 to clarify requirements
5. **Iterate** through phases 2-5, verifying at each stage

## File Structure

```
.github/skills/fullstack-survey-app/
├── SKILL.md                    ← Main methodology (read first!)
├── architecture.md             ← System design & data flow
├── README.md                   ← This file
└── templates/
    ├── backend-config.py       ← Template for config.py
    ├── frontend-store.js       ← Template for SurveyStore.js
    └── api-client.js           ← Template for surveyApi.js
```

## Key Decisions Explained

| Question | Answer | Why |
|----------|--------|-----|
| Backend? | FastAPI | Modern, fast, excellent for data APIs |
| Frontend? | React + Hooks | Industry standard, large ecosystem |
| State Mgmt? | MobX | Simpler than Redux for forms |
| Database? | SQLite | Zero setup; can upgrade to PostgreSQL later |
| Layout? | Monorepo | Easier to share code, single git repo |
| Test? | Integration test | Full workflow verification |

## Success Criteria

Before each phase completes, verify:

- Phase 1: Plan accepted ✓
- Phase 2: Backend runs, API returns data ✓
- Phase 3: Frontend builds, form renders ✓
- Phase 4: End-to-end workflow works, data saved ✓
- Phase 5: All docs written, git ready ✓

## Next Steps After Completing

Once your survey app is done:
1. **Add Authentication** — JWT, user accounts
2. **Add Admin Panel** — Create/edit surveys, view responses
3. **Add Analytics** — Charts, statistics, export
4. **Deploy** — Docker, AWS, Heroku, Vercel
5. **Scale** — Multi-user, real-time updates

## Support

For issues or questions:
- See "Troubleshooting Decision Tree" in SKILL.md
- Check the example prompts that triggered this skill
- Review the mini-survey app repo at `/workspaces/otus-AI/`

---

**Version**: 1.0  
**Last Updated**: April 26, 2026  
**Status**: ✅ Tested with Mini-Survey app  
**Author**: GitHub Copilot  
