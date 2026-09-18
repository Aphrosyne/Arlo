# N 网标签基线

本文档记录当前准备整理的 Nexus Mods 完整标签清单，作为后续改为全中文标签前的基线。

- 记录日期：2026-09-19
- 来源：用户提供的 N 网近期开启的完整标签列表
- 说明：本文件只记录标签名称，不记录 N 网显示的数量。
- 当前状态：第一版主分类已确认；辅助标签、作者/来源维度和中文名称仍可继续细化。

## 英文标签

- Alchemy
- Animation
- Armour
- Armour - Shields
- Audio
- Body, Face, and Hair
- Bug Fixes
- Buildings
- Cheats and God items
- Cities, Towns, Villages, and Hamlets
- Clothing and Accessories
- Collectables, Treasure Hunts, and Puzzles
- Combat
- Crafting
- Creatures and Mounts
- Dungeons
- Environmental
- Followers & Companions
- Followers & Companions - Creatures
- Gameplay
- Guilds/Factions
- Immersion
- Items and Objects - Player
- Items and Objects - World
- Locations -  New
- Locations - Vanilla
- Magic - Gameplay
- Magic - Spells & Enchantments
- Miscellaneous
- Modders Resources
- Models and Textures
- NPC
- Overhauls
- Patches
- Player homes
- Presets - ENB and ReShade
- Quests and Adventures
- Races, Classes, and Birthsigns
- Save Games
- Shouts
- Skills and Leveling
- Stealth
- User Interface
- Utilities
- Visuals and Graphics
- VR
- Weapons
- Weapons and Armour

## 英中对照与筛选

中文列是初步候选译名，不代表最终命名；可在“筛选/修改意见”列记录保留、删除、合并或改名决定。

| 英文标签 | 中文候选 | 筛选/修改意见 |
| --- | --- | --- |
| Alchemy | 炼金术 | |
| Animation | 动画 | |
| Armour | 护甲 | |
| Armour - Shields | 护甲 - 盾牌 | |
| Audio | 音频 | |
| Body, Face, and Hair | 身体、面部与头发 | |
| Bug Fixes | 错误修复 | |
| Buildings | 建筑 | |
| Cheats and God items | 作弊与神器 | |
| Cities, Towns, Villages, and Hamlets | 城市、城镇、村庄与小村落 | |
| Clothing and Accessories | 服装与配饰 | |
| Collectables, Treasure Hunts, and Puzzles | 收藏品、寻宝与谜题 | |
| Combat | 战斗 | |
| Crafting | 制作 | |
| Creatures and Mounts | 生物与坐骑 | |
| Dungeons | 地下城 | |
| Environmental | 环境 | |
| Followers & Companions | 随从与同伴 | |
| Followers & Companions - Creatures | 随从与同伴 - 生物 | |
| Gameplay | 游戏玩法 | |
| Guilds/Factions | 公会/阵营 | |
| Immersion | 沉浸体验 | |
| Items and Objects - Player | 物品与对象 - 玩家 | |
| Items and Objects - World | 物品与对象 - 世界 | |
| Locations -  New | 地点 - 新增 | |
| Locations - Vanilla | 地点 - 原版 | |
| Magic - Gameplay | 魔法 - 玩法 | |
| Magic - Spells & Enchantments | 魔法 - 法术与附魔 | |
| Miscellaneous | 杂项 | |
| Modders Resources | Mod 制作者资源 | |
| Models and Textures | 模型与纹理 | |
| NPC | NPC | |
| Overhauls | 大修 | |
| Patches | 补丁 | |
| Player homes | 玩家住宅 | |
| Presets - ENB and ReShade | 预设 - ENB 与 ReShade | |
| Quests and Adventures | 任务与冒险 | |
| Races, Classes, and Birthsigns | 种族、职业与出生星座 | |
| Save Games | 存档 | |
| Shouts | 龙吼 | |
| Skills and Leveling | 技能与升级 | |
| Stealth | 潜行 | |
| User Interface | 用户界面 | |
| Utilities | 实用工具 | |
| Visuals and Graphics | 视觉效果与图形 | |
| VR | VR | |
| Weapons | 武器 | |
| Weapons and Armour | 武器与护甲 | |

### 筛选规则

- 中文候选仅用于讨论，最终名称以确认后的结果为准。
- 可以在意见列标记“保留”“删除”“合并”或直接填写新的中文名称。
- `NPC`、`VR`、`ENB`、`ReShade`、`Mod` 等术语是否保留英文，待筛选时统一决定。

## 基于本地资源库的第一版精简方案（待审核）

本节根据以下事实整理，暂不直接修改 `tags.json` 或数据库：

- 当前路线图阶段 1：标签应精简，不能阻塞内容单元建立；系统状态不作为普通内容标签。
- 用户提供的本地分类目录：实际主结构集中在装备物品、玩法系统、NPC 生物、任务地点、角色美化、动画动作、物理系统、世界环境、UI、音效、画面渲染、补丁兼容等方向。
- 项目根目录 `tags.json`：保留其中有实际使用价值的本地细分标签，但重新区分内容标签、辅助维度和系统状态。

### 一、建议保留的主分类

这些主分类对应本地资源库中已经存在的稳定分类，建议作为第一版中文标签的骨架：

| 主分类 | 建议 | 说明 |
| --- | --- | --- |
| 核心框架 | 保留 | 对应框架、前置、资源依赖和 Mod 制作者资源。 |
| 补丁兼容 | 保留 | 合并错误修复与补丁，不再拆成两个近似标签。 |
| 角色美化 | 保留 | 合并身体、面部、头发和角色预设方向。 |
| 装备物品 | 保留 | 合并护甲、盾牌、服装及玩家/世界物品。 |
| 武器 | 保留 | 武器与武器护甲合并，具体类型用辅助标签表达。 |
| 动画动作 | 保留 | 对应动画、姿势和动作资源。 |
| 物理系统 | 保留 | 本地资源库中的实际分类，属于本地补充标签。 |
| 世界环境 | 保留 | 对应建筑、环境和世界场景资源。 |
| 玩法系统 | 保留 | 合并战斗、制作、魔法、技能、潜行等玩法方向。 |
| 任务地点 | 保留 | 合并任务、地点、地下城、城市和玩家住宅。 |
| NPC 与生物 | 保留 | 合并 NPC、随从、生物、坐骑和种族方向。 |
| UI 界面 | 保留 | 对应用户界面和菜单工具。 |
| 音效音乐 | 保留 | 合并音频、音效和音乐。 |
| 画面渲染 | 保留 | 合并视觉效果、图形、ENB/ReShade、模型与纹理。 |
| 其他杂项 | 保留 | 仅作为无法稳定归类内容的回退分类。 |

“待整理”“输出文件”“归档目录”属于工作流或物理位置，不建议做成内容标签；“实验室”是否作为本地特殊分类保留，先不纳入默认主分类，待审核。

### 二、N 网标签归并关系

下表是第一版建议，不代表自动迁移规则。一个资源实际可能同时拥有一个主分类和若干细分标签。

| 建议主分类 | 合并纳入的 N 网标签 | 处理意见 |
| --- | --- | --- |
| 核心框架 | Modders Resources；Utilities | 合并为一个主分类，不保留两个近义大类。 |
| 补丁兼容 | Bug Fixes；Patches | 合并。 |
| 角色美化 | Body, Face, and Hair；Presets - ENB and ReShade 中的角色预设部分 | 角色预设归入这里；ENB/ReShade 本身归入画面渲染。 |
| 装备物品 | Armour；Armour - Shields；Clothing and Accessories；Items and Objects - Player；Items and Objects - World | 护甲与盾牌合并；玩家/世界物品不再单独拆分。 |
| 武器 | Weapons；Weapons and Armour | 合并；保留单手、双手、弓、法杖等细分标签。 |
| 动画动作 | Animation | 保留为主分类。 |
| 世界环境 | Buildings；Environmental | 合并建筑与环境。 |
| 玩法系统 | Alchemy；Cheats and God items；Combat；Crafting；Gameplay；Guilds/Factions；Immersion；Magic - Gameplay；Magic - Spells & Enchantments；Overhauls；Shouts；Skills and Leveling；Stealth | 统一归入玩法系统，具体魔法、战斗、技能等用细分标签表达。 |
| 任务地点 | Cities, Towns, Villages, and Hamlets；Collectables, Treasure Hunts, and Puzzles；Dungeons；Locations - New；Locations - Vanilla；Player homes；Quests and Adventures | 合并为任务地点；不再按地点类型拆成多个主标签。 |
| NPC 与生物 | Creatures and Mounts；Followers & Companions；Followers & Companions - Creatures；NPC；Races, Classes, and Birthsigns | 合并；随从与野兽保留为细分标签。 |
| UI 界面 | User Interface | 保留为主分类。 |
| 音效音乐 | Audio | 保留为主分类。 |
| 画面渲染 | Models and Textures；Visuals and Graphics；Presets - ENB and ReShade 中的 ENB/ReShade 部分 | 合并视觉、图形和画面预设；模型与纹理不单独作为主分类。 |
| 其他杂项 | Miscellaneous | 保留为回退分类。 |
| 暂不纳入第一版 | Save Games；VR | 当前本地分类目录中缺乏稳定对应关系，先不作为默认标签；以后有实际资源再补。 |

### 三、`tags.json` 的本地标签调整建议

| 当前分类 | 建议处理 | 第一版结果 |
| --- | --- | --- |
| NPC生物 | 分类名可改为“NPC 与生物” | 保留“随从”“野兽”。 |
| 作者 | 独立辅助维度 | 保留，不与内容主分类合并。 |
| 来源 | 独立辅助维度 | 保留，不与内容主分类合并。 |
| 武器 | 去掉泛化的“武器”标签 | 保留“动作武器”“单手”“双手”“弓”“法杖”；主分类已经表达武器。 |
| 状态 | 从普通标签中移出 | “已汉化”“已测试”“待测试”改作为系统状态，不计入内容标签。 |
| 玩法 | 合并重复粒度 | 保留“大修”“战斗”“技能”“法术”；“自定义技能”并入“技能”，“特效”可归入“画面渲染”，“祝福”暂归入“法术”。 |
| 装备物品 | 保留高频和有区分度的细分项 | 保留“UBE”“内衣”“护甲”“服装”“饰品”“高跟鞋”；“合集”视为整理属性，“幻想”“现代”暂列可选风格，“裸露”列为可选内容提示。 |
| 角色美化 | 合并预设类型 | “BS预设”“RM预设”合并为“预设”；保留“发型”“皮肤”“纹身”。 |

### 四、已确认的第一版主分类集合

#### 主分类（已确认）

- [x] 核心框架
- [x] 补丁兼容
- [x] 角色美化
- [x] 装备物品
- [x] 武器
- [x] 动画动作
- [x] 物理系统
- [x] 世界环境
- [x] 玩法系统
- [x] 任务地点
- [x] NPC 与生物
- [x] UI 界面
- [x] 音效音乐
- [x] 画面渲染
- [x] 其他杂项

#### 第一版标签结构

- 每个内容单元使用一个主分类；主分类是标签，不是物理目录。
- 一个内容单元可以拥有多个辅助标签。
- 作者、来源属于独立辅助维度，不与主分类合并。
- 当前只确认主分类基线，辅助标签的完整清单和命名规则仍待后续审核。
#### 辅助标签与维度

- NPC 与生物：随从、野兽
- 武器：动作武器、单手、双手、弓、法杖
- 玩法系统：大修、战斗、技能、法术
- 装备物品：UBE、内衣、护甲、服装、饰品、高跟鞋
- 角色美化：预设、发型、皮肤、纹身
- 辅助维度：作者、来源
- 可选维度：合集、幻想、现代、裸露、祝福、特效

#### 不作为普通内容标签

- 已汉化、已测试、待测试：系统状态
- 待整理、输出文件、归档目录：工作流或物理位置
- Save Games、VR：当前缺少本地资源库依据，暂缓

以上主分类已确认；辅助标签与维度仍是候选结果。确认辅助标签前不修改 `tags.json`，也不执行已有资源的批量重分类。
