-- More Dockyards Per Ship - "Naval Blitz"
-- Raises the maximum number of naval dockyards you can assign to a single
-- ship production line, so you can pour your shipyards into a few lines and
-- mass-produce a fleet.
--
-- Vanilla defaults (NProduction):
--   CAPITAL_SHIP_MAX_NAV_FACTORIES_PER_LINE = 5    (battleships, carriers, cruisers...)
--   DEFAULT_MAX_NAV_FACTORIES_PER_LINE      = 10   (screens: destroyers etc. + submarines)
--   CONVOY_MAX_NAV_FACTORIES_PER_LINE       = 15   (convoys)
--   MAX_NAV_FACTORIES_PER_LINE              = 15   (overall ceiling for ALL lines)
--
-- The overall ceiling (MAX_NAV_FACTORIES_PER_LINE) is the hard cap that the
-- per-type limits are clamped to, so it must be raised as well.
--
-- Want a different cap? Change every 50 below to the number you like.
-- (Setting it absurdly high effectively removes the limit.)

NDefines.NProduction.MAX_NAV_FACTORIES_PER_LINE              = 50
NDefines.NProduction.CAPITAL_SHIP_MAX_NAV_FACTORIES_PER_LINE = 50
NDefines.NProduction.DEFAULT_MAX_NAV_FACTORIES_PER_LINE      = 50
NDefines.NProduction.CONVOY_MAX_NAV_FACTORIES_PER_LINE       = 50

-- Floating harbours share the capital-ship cap in vanilla. This extra key is
-- harmless if the engine does not use it on your version.
NDefines.NProduction.FLOATING_HARBOR_MAX_NAV_FACTORIES_PER_LINE = 50
