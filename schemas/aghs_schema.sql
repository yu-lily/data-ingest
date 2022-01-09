CREATE TABLE matches (
    id BIGINT PRIMARY KEY,
    didWin BOOLEAN,
    durationSeconds INTEGER,
    startDateTime TIMESTAMP,
    endDateTime TIMESTAMP,
    clusterId SMALLINT,
    lobbyType SMALLINT,
    numKills SMALLINT,
    numDeaths SMALLINT,
    numHumanPlayers SMALLINT,
    gameMode SMALLINT,
    replaySalt INTEGER,
    difficulty TEXT,
    depth SMALLINT,
    seed INTEGER,
    battlePoints INTEGER,
    score INTEGER,
    arcaneFragments INTEGER,
    goldBags INTEGER,
    regionId SMALLINT
);

CREATE TABLE players(
    matchId BIGINT,
    playerSlot SMALLINT,
    steamAccountId BIGINT,
    isVictory BOOLEAN,
    heroId SMALLINT,
    deaths SMALLINT,
    leaverStatus SMALLINT,
    numLastHits INTEGER,
    goldPerMinunte SMALLINT,
    networth INTEGER,
    experiencePerMinute SMALLINT,
    level SMALLINT,
    goldSpent INTEGER,
    partyId INTEGER,
    item0Id INTEGER,
    item1Id INTEGER,
    item2Id INTEGER,
    item3Id INTEGER,
    item4Id INTEGER,
    item5Id INTEGER,
    neutral0Id INTEGER,
    arcaneFragments INTEGER,
    bonusArcaneFragments INTEGER,
    goldBags INTEGER,
    neutralItemId INTEGER,
    PRIMARY KEY(matchId, playerSlot),
    FOREIGN KEY(matchId) REFERENCES matches(id)
);

CREATE TABLE playerDepthList(
    matchId BIGINT,
    playerSlot SMALLINT,
    depth SMALLINT,
    steamAccountId BIGINT,
    numDeaths SMALLINT,
    goldBags SMALLINT,
    kills SMALLINT,
    level SMALLINT,
    networth INTEGER,
    rarity SMALLINT,
    selectedRewardAbilityId INTEGER,
    unSelectedRewardAbilityId1 INTEGER,
    unSelectedRewardAbilityId2 INTEGER,
    selectedRewardImageAbilityId INTEGER,
    PRIMARY KEY(matchId, playerSlot, depth),
    FOREIGN KEY(matchId) REFERENCES matches(id),
    FOREIGN KEY(matchId, playerSlot) REFERENCES players(matchId, playerSlot)
);

CREATE TABLE playerBlessings(
    matchId BIGINT,
    playerSlot SMALLINT,
    steamAccountId BIGINT,
    type TEXT,
    value INTEGER,
    PRIMARY KEY(matchId, playerSlot, type),
    FOREIGN KEY(matchId) REFERENCES matches(id),
    FOREIGN KEY(matchId, playerSlot) REFERENCES players(matchId, playerSlot)
);

CREATE TABLE depthList(
    matchId BIGINT,
    depth SMALLINT,
    selectedElite BOOLEAN,
    selectedEncounter TEXT,
    selectedEncounterType SMALLINT,
    selectedHidden BOOLEAN,
    selectedReward TEXT,
    unselectedElite BOOLEAN,
    unselectedEncounter TEXT,
    unselectedHidden BOOLEAN,
    unselectedReward TEXT,
    PRIMARY KEY(matchId, depth),
    FOREIGN KEY(matchId) REFERENCES matches(id)
);

CREATE TABLE ascensionAbilities(
    matchId BIGINT,
    depth SMALLINT,
    type TEXT,
    abilityId SMALLINT,
    modifierId SMALLINT,
    PRIMARY KEY(matchId, depth, type),
    FOREIGN KEY(matchId) REFERENCES matches(id),
    FOREIGN KEY(matchId, depth) REFERENCES depthList(matchId, depth)
);

CREATE TABLE const_customAbilites(
    id SMALLINT,
    name TEXT,
    abilityName TEXT,
    displayName TEXT,
    description TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE const_heroes(
    id SMALLINT,
    name TEXT,
    displayName TEXT,
    shortName TEXT,
    aliases TEXT[],
    PRIMARY KEY(id)
);

CREATE TABLE const_abilities(
    abilityId SMALLINT,
    heroId SMALLINT,
    slot SMALLINT,
    name TEXT,
    displayName TEXT,
    PRIMARY KEY(abilityId, heroId, slot),
    FOREIGN KEY(heroId) REFERENCES const_heroes(id)
);