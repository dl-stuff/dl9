| Field                            | Type         | Notes                                        |
| -------------------------------- | ------------ | -------------------------------------------- |
| _Id                              | int          | int id                                       |
| _Type                            | AfflictType  | affliction type                              |
| _Text                            | str          | only way to know bleed                       |
| _TextEx                          | str          | alt text                                     |
| _BlockExaustFlag                 | BlockExhaust | no pewpew when skill/shift                   |
| _InternalFlag                    | BuffFlag     | 1=no icon, 2=no count                        |
| _UniqueIcon                      | int          | unique icon id in InGameBuffUI               |
| _ResistBuffReset                 | bool         | do not refersh buff                          |
| _ResistDebuffReset               | bool         | do not refersh debuff                        |
| _UnifiedManagement               | bool         | ???                                          |
| _Overwrite                       | int          | overwrite same id                            |
| _OverwriteIdenticalOwner         | int          | overwrite same id & owner                    |
| _OverwriteGroupId                | int          | overwrite same group & leq                   |
| _MaxDuplicatedCount              | int          | max stack per adv                            |
| _UsePowerUpEffect                | int          | ???                                          |
| _NotUseStartEffect               | int          | ??, always 0                                 |
| _StartEffectCommon               | str          | ?, effect stuff                              |
| _StartEffectAdd                  | str          | ?, effect stuff, always ""                   |
| _LostOnDragon                    | int          | turn off on shift                            |
| _RestoreOnReborn                 | int          | restore on reborn                            |
| _Rate                            | int          | chance out of 100                            |
| _EfficacyType                    | BuffEff      | effect against buffs (e.g. dispel)           |
| _RemoveConditionId               | int          | buff id removed                              |
| _DebuffCategory                  | int          | 1=corrosion                                  |
| _RemoveDebuffCategory            | int          | ?, remove given category                     |
| _DurationSec                     | float        | duration                                     |
| _DurationNum                     | int          | number of uses, ignore if not act mod        |
| _MinDurationSec                  | float        | min duration                                 |
| _DurationTimeScale               | int          | ??, something for UI                         |
| _IsAddDurationNum                | bool         | refresh adds to _DurationNum                 |
| _MaxDurationNum                  | int          | max number of uses                           |
| _CoolDownTimeSec                 | float        | cd before buff can reactivate, e.g. peony    |
| _RemoveAciton                    | int          | ???                                          |
| _SlipDamageIntervalSec           | float        | slip damage interval                         |
| _SlipDamageFixed                 | int          | fixed                                        |
| _SlipDamageRatio                 | float        | percent                                      |
| _SlipDamageMax                   | int          | maximum                                      |
| _SlipDamagePower                 | float        | power                                        |
| _SlipDamageGroup                 | int          | 1=corrosion(boss), 2=corrosion(print)        |
| _RateIncreaseByTime              | float        | corrosion ramp rate                          |
| _RateIncreaseDuration            | float        | corrosion ramp interval                      |
| _RegenePower                     | float        | regen heal power                             |
| _DebuffGrantRate                 | float        | debuff rate up                               |
| _EventProbability                | int          | ??, blind chance                             |
| _EventCoefficient                | float        | ???                                          |
| _DamageCoefficient               | float        | damage take coef                             |
| _TargetAction                    | int          | ??, always 0                                 |
| _TargetElemental                 | int          | element bitmap                               |
| _ConditionAbs                    | int          | ??, always 0                                 |
| _ConditionDebuff                 | int          | if debuff id exists, i.e. Ieyasu             |
| _RateHP                          | float        | max hp de/buff                               |
| _RateAttack                      | float        | strength de/buff                             |
| _RateDefense                     | float        | defense de/buff                              |
| _RateDefenseB                    | float        | defense de/buff, -0.3 cap                    |
| _RateCritical                    | float        | crit rate de/buff                            |
| _RateSkill                       | float        | skill damage de/buff                         |
| _RateBurst                       | float        | force strike de/buff                         |
| _RateRecovery                    | float        | recovery potency de/buff                     |
| _RateRecoverySp                  | float        | skill haste de/buff                          |
| _RateRecoverySpExceptTargetSkill | int          | skill idx bitmap, 0=gets haste               |
| _RateRecoveryDp                  | float        | dragon haste de/buff                         |
| _RateRecoveryUtp                 | float        | utp haste de/buff                            |
| _RateAttackSpeed                 | float        | attack speed de/buff                         |
| _RateChargeSpeed                 | float        | fs marker speed de/buff                      |
| _RateBurstSpeed                  | float        | fs execute speed de/buff                     |
| _MoveSpeedRate                   | float        | move speed de/buff                           |
| _RatePoison                      | float        | aff resist de/buff                           |
| _RateBurn                        | float        | ..                                           |
| _RateFreeze                      | float        | ..                                           |
| _RateParalysis                   | float        | ..                                           |
| _RateDarkness                    | float        | ..                                           |
| _RateSwoon                       | float        | ..                                           |
| _RateCurse                       | float        | ..                                           |
| _RateSlowMove                    | float        | ..                                           |
| _RateSleep                       | float        | ..                                           |
| _RateFrostbite                   | float        | ..                                           |
| _RateFlashheat                   | float        | ..                                           |
| _RateCrashWind                   | float        | ..                                           |
| _RateDarkAbs                     | float        | ..                                           |
| _RateDestroyFire                 | float        | ..                                           |
| _RatePoisonKiller                | float        | aff killer de/buff                           |
| _RateBurnKiller                  | float        | ..                                           |
| _RateFreezeKiller                | float        | ..                                           |
| _RateParalysisKiller             | float        | ..                                           |
| _RateDarknessKiller              | float        | ..                                           |
| _RateSwoonKiller                 | float        | ..                                           |
| _RateCurseKiller                 | float        | ..                                           |
| _RateSlowMoveKiller              | float        | ..                                           |
| _RateSleepKiller                 | float        | ..                                           |
| _RateFrostbiteKiller             | float        | ..                                           |
| _RateFlashheatKiller             | float        | ..                                           |
| _RateCrashWindKiller             | float        | ..                                           |
| _RateDarkAbsKiller               | float        | ..                                           |
| _RateDestroyFireKiller           | float        | ..                                           |
| _RateFire                        | float        | ele res de/buff                              |
| _RateWater                       | float        | ..                                           |
| _RateWind                        | float        | ..                                           |
| _RateLight                       | float        | ..                                           |
| _RateDark                        | float        | ..                                           |
| _EnhancedFire                    | float        | ele dmg 1 de/buff, always 0                  |
| _EnhancedWater                   | float        | ..                                           |
| _EnhancedWind                    | float        | ..                                           |
| _EnhancedLight                   | float        | ..                                           |
| _EnhancedDark                    | float        | ..                                           |
| _EnhancedFire2                   | float        | ele dmg de/buff                              |
| _EnhancedWater2                  | float        | ..                                           |
| _EnhancedWind2                   | float        | ..                                           |
| _EnhancedLight2                  | float        | ..                                           |
| _EnhancedDark2                   | float        | ..                                           |
| _EnhancedNoElement               | float        | ele dmg de/buff                              |
| _RateMagicCreature               | float        | tribe res de/buff                            |
| _RateNatural                     | float        | ..                                           |
| _RateDemiHuman                   | float        | ..                                           |
| _RateBeast                       | float        | ..                                           |
| _RateUndead                      | float        | ..                                           |
| _RateDeamon                      | float        | ..                                           |
| _RateHuman                       | float        | ..                                           |
| _RateDragon                      | float        | ..                                           |
| _RateDamageCut                   | float        | dmg reduce by %                              |
| _RateDamageCut2                  | float        | dmg reduce by %, always 0                    |
| _RateDamageCutB                  | float        | dmg reduce by %                              |
| _RateWeakInvalid                 | float        | ???                                          |
| _HealInvalid                     | int          | heal block, e.g. zhu bajie                   |
| _TensionUpInvalid                | int          | energy block, e.g. snorwin                   |
| _ValidRegeneHP                   | float        | slip damge was regen HP                      |
| _ValidRegeneSP                   | float        | slip damge was regen SP                      |
| _ValidRegeneDP                   | float        | slip damge was regen DP                      |
| _ValidSlipHp                     | float        | slip damge was degen HP                      |
| _RequiredRecoverHp               | int          | corrosion reset heal thresh                  |
| _RateGetHpRecovery               | float        | incoming hp recovery mod                     |
| _UniqueRegeneSp01                | float        | slip damage was regen sp s2                  |
| _AutoRegeneS1                    | float        | slip damage was regen sp s1                  |
| _AutoRegeneSW                    | float        | ???                                          |
| _RateReraise                     | float        | ??, reborn related                           |
| _RateArmored                     | float        | knockback res                                |
| _RateDamageShield                | float        | 1 use shield                                 |
| _RateDamageShield2               | float        | ..                                           |
| _RateDamageShield3               | float        | ..                                           |
| _RateSacrificeShield             | float        | life shield                                  |
| _SacrificeShieldType             | int          | 1=use max hp                                 |
| _Malaise01                       | int          | enervate                                     |
| _Malaise02                       | int          | ..                                           |
| _Malaise03                       | int          | ..                                           |
| _RateNicked                      | float        | dull                                         |
| _CurseOfEmptiness                | int          | nihility                                     |
| _CurseOfEmptinessInvalid         | bool         | nihility immune                              |
| _TransSkill                      | float        | skill shift                                  |
| _GrantSkill                      | int          | ActionGrant                                  |
| _DisableAction                   | int          | -1=cannot do anything                        |
| _DisableActionFlags              | int          | ??, always 0                                 |
| _DisableMove                     | int          | -1=cannot move                               |
| _InvincibleLv                    | int          | ??, always 0                                 |
| _AutoAvoid                       | float        | ?, avoid rate, see faris                     |
| _ComboShift                      | bool         | change combo actions                         |
| _EnhancedBurstAttack             | int          | change burst action                          |
| _EnhancedSkill1                  | int          | change skill 1                               |
| _EnhancedSkill2                  | int          | change skill 2                               |
| _EnhancedSkillWeapon             | int          | change weapon skill                          |
| _EnhancedCritical                | float        | crit damage buff                             |
| _Tension                         | int          | energy                                       |
| _Inspiration                     | int          | inspiration                                  |
| _Cartridge                       | int          | cartridge, ilia                              |
| _ModeStack                       | bool         | mode stacks, catherine                       |
| _StackData                       | int          | ?, buff stack data, pandora                  |
| _StackNum                        | int          | ?, buff stack data, pandora                  |
| _Sparking                        | int          | electrified, albert                          |
| _RateHpDrain                     | float        | hp drain %                                   |
| _HpDrainLimitRate                | float        | hp drain cap                                 |
| _SelfDamageRate                  | float        | ???                                          |
| _HpConsumptionRate               | float        | self hp damage %                             |
| _HpConsumptionCoef               | float        | ??, always 0                                 |
| _RemoveTrigger                   | bool         | proc REMOVE_BUFF_TRIGGER_BOMB                |
| _DamageLink                      | str          | proc hitattr when damaged                    |
| _AdditionAttack                  | str          | overdamage hitattr                           |
| _AdditionAttackHitEffect         | str          | overdamage effect                            |
| _ExtraBuffType                   | int          | special enemy buffs                          |
| _EnhancedSky                     | bool         | ??, enhanced skill?                          |
| _InvalidBuffId                   | int          | ???                                          |
| _ModifyChargeLevel               | int          | changes number of charge level char has      |
| _Hiding                          | int          | BR dagger hide                               |
| _LevelUpId                       | int          | level up to this buff when refresh           |
| _LevelDownId                     | int          | level down to this buff when timeout/consume |
| _ExcludeFromBuffExtension        | bool         | ignore bufftime                              |