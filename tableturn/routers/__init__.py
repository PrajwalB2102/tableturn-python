"""Routes parse and delegate; they hold no rules. The request-scoped dependencies live
here, so nothing below the routers (services, rules, settings, db) imports FastAPI."""
