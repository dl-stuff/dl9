| Field                            | Type          | Notes                                    |
| -------------------------------- | ------------- | ---------------------------------------- |
| _Id                              | str           | string _Id of this hit label             |
| _FontEffect                      | str           | ???                                      |
| _HitExecType                     | HitExec       | affects hit count proc                   |
| _TargetGroup                     | HitTarget     | target(s) of this hit                    |
| _TargetElemental                 | int           | per ele target, e.g. nevin s1            |
| _Elemental01                     | int           | ele type override, e.g. grimnir a1       |
| _Elemental02                     | int           | ???                                      |
| _Attributes02                    | bool          | ???                                      |
| _Attributes03                    | bool          | ???                                      |
| _LookToDamageType                | int           | ??, only in BR_TOUCH_HIT                 |
| _Attributes04                    | bool          | ???                                      |
| _Attributes05                    | bool          | ???                                      |
| _Attributes07                    | bool          | ??, always 1                             |
| _Attributes08                    | bool          | ???                                      |
| _AttrIgnoreBarrier               | bool          | ignores enemy shields                    |
| _AttrNoReaction                  | bool          | no knockback                             |
| _AttrShare                       | bool          | ??, always 0                             |
| _AttrCancelBind                  | bool          | ??, always 0                             |
| _AttrDragon                      | bool          | uses dragon damage (no dracolith)        |
| _DamageAdjustment                | float         | damage modifier                          |
| _ToOdDmgRate                     | float         | mod for filling OD                       |
| _ToBreakDmgRate                  | float         | mod for depleting OD                     |
| _ToEightDownRate                 | float         | ?, persona all-out attack                |
| _AdditionCritical                | float         | hitattr crit rate                        |
| _IsAdditionalAttackToEnemy       | bool          | overdamage flag                          |
| _IsDamageMyself                  | bool          | self damage flag                         |
| _SetCurrentHpRate                | float         | set current hp to %                      |
| _ConsumeHpRate                   | float         | reduce current hp by %                   |
| _DamageSelfUpFromBuffCountBuffId | int           | actcond, _ConsumeHpRate *= stack number  |
| _RecoveryValue                   | int           | heal power                               |
| _AdditionRecoverySp              | int           | skill points (sp)                        |
| _RecoverySpRatio                 | float         | sp %, no haste                           |
| _RecoverySpSkillIndex            | bool          | sp target skill 1, 0 if all              |
| _RecoverySpSkillIndex2           | bool          | sp target skill 2, 0 if all              |
| _AdditionRecoveryDpPercentage    | float         | dp %, no dhaste, e.g. nimis              |
| _RecoveryDragonTime              | float         | dragon time, e.g. nimis                  |
| _AdditionRecoveryDpLv1           | int           | dragon points (dp)                       |
| _AdditionRecoveryDpAbility       | int           | ??, always 0                             |
| _RecoveryEp                      | int           | megaman ammo points                      |
| _RecoveryCP                      | int           | chara unique gauge points                |
| _RecoveryCPIndex                 | int           | ??, maybe for multi chara gauge          |
| _RecoveryCPEveryHit              | int           | ignore once per act rule for CP          |
| _AdditionActiveGaugeValue        | int           | granzal gauge points                     |
| _AdditionRecoveryUtp             | int           | unique transform points (utp)            |
| _AddUtp                          | int           | utp, no dhaste when <0                   |
| _IgnoreHitCountAddition          | bool          | force no add hit                         |
| _IgnoreFirstHitCheck             | bool          | ignore once per act rule                 |
| _FixedDamage                     | int           | do this much damage exactly              |
| _CurrentHpRateDamage             | int           | ??, always 0                             |
| _HpDrainRate                     | float         | hp drain % capped                        |
| _HpDrainRate2                    | float         | hp drain %                               |
| _HpDrainLimitRate                | float         | hp drain cap                             |
| _HpDrainAttribute                | str           | hp drain HitAttr, has the heal target    |
| _DamageCounterCoef               | float         | damage counter mod, follows HitExec      |
| _CrisisLimitRate                 | float         | crisis mod, *= %lost^2                   |
| _DamageDispDelaySec              | float         | ?, delay on dmg num visual               |
| _IsDisableHealSpOnCurse          | int           | disable sp gain if cursed                |
| _ActionCondition1                | int           | ActionCondition (buff/debuff/etc)        |
| _HeadText                        | str           | text label                               |
| _BattleLogText                   | str           | battle log label, dead post v2.6         |
| _ActionGrant                     | int           | ?, always 0, ActionGrant                 |
| _AuraId                          | int           | AuraData                                 |
| _AuraMaxLimitLevel               | int           | max level for team aura                  |
| _KillerState1                    | KillerState   | killer state type                        |
| _KillerState2                    | KillerState   | killer state type                        |
| _KillerState3                    | KillerState   | killer state type                        |
| _KillerStateDamageRate           | float         | killer mod, applied once                 |
| _KillerStateRelease              | int           | ??, always 0                             |
| _DamageUpRateByBuffCount         | float         | xander/karina buff count mod             |
| _DamageUpDataByBuffCount         | int           | BuffCountData, e.g. lapis                |
| _SplitDamageCount                | int           | in raids, show x dmg numbers             |
| _SplitDamageCount2               | int           | ??, prob same as above?                  |
| _ArmorBreakLv                    | int           | ??, superarmor bypass lv                 |
| _InvincibleBreakLv               | int           | ??, shield bypass lv                     |
| _KnockBackType                   | KnockBackType | direction of knockback                   |
| _KnockBackDistance               | float         | kb distance                              |
| _KnockBackDependsOnMass          | bool          | ??, enemy has mass, unsure about formula |
| _KnockBackDurationSec            | float         | ??, kb speed kinda                       |
| _UseDamageMotionTimeScale        | bool          | ???                                      |
| _DamageMotionTimeScale           | float         | ???                                      |
| _HitConditionType                | PHitCond      | ?, laranoa=1, others=2 or 0              |
| _HitConditionP1                  | int           | num of targets                           |
| _HitConditionP2                  | int           | num of targets                           |
| _IsAddCombo                      | int           | force add combo                          |
| _BlastHeight                     | float         | ???                                      |
| _BlastAngle                      | float         | ???                                      |
| _BlastGravity                    | float         | ???                                      |
"""