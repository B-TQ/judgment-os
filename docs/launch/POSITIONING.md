# Positioning / 定位

**Test what your agent's Skills actually change. / 用对照实验，看看 Skill 到底改变了什么。**

The principle is “Skills should expand intelligence, not constrain it.” It is a design aim, not an efficacy result. The project name is not an operating-system claim.

理念是“Skill 应扩展智能，而不是限制它”。这是设计目标，不是已经验证的效果结论；项目名称不代表它是操作系统。

## Problem → insight → solution → evidence

**Problem.** An optional template can become a poor default for an individual task. We do not infer widespread degradation from this possibility.

**Insight.** Another layer of instructions can also add cost or no benefit. Compare against task-only and a short reminder, not just a deliberately weak baseline.

**Solution.** v0.7 freezes shared requirements, collects real answers, runs declared checks and separates blinded review phases. Its optional meta-Skill offers bounded adaptation in natural language.

**Evidence.** The eight-case follow-up did not meet the adoption rule. C–D was 1/7/0; the win was a one-word overrun. Software tests support tool behavior, not agent efficacy.

**问题：** 可选模板可能不适合某个任务，但不能由此断言 Skill 普遍导致退化。

**观察：** 再叠加长提示词也未必有用，应同时比较原始任务和一句提醒，不能故意削弱基线。

**方案：** v0.7 固定共同要求、收集真实回答、执行声明检查，并分开匿名评审轮次；可选元 Skill 只提供自然语言指导。

**证据：** 八题后续实验未达到采用门槛；C–D 为 1/7/0，唯一胜出是字数差一词。软件测试只能支持工具行为。

## Mechanisms, not invented competitive advantages / 比机制，不虚构优势

| Approach / 类型 | Mechanism / 机制 | Boundary / 边界 |
| --- | --- | --- |
| Domain Skill / 领域 Skill | Task expertise, instructions, optional assets / 专业知识、指导与资源 | Quality and fit vary / 质量与适用性因任务而异 |
| Prompt enhancement / 提示词增强 | Adds guidance to context / 向上下文增加指导 | Needs comparison; no automatic effect / 仍需对照验证 |
| Skill coordinator / Skill 协调器 | May route or sequence Skills / 可调度或编排 Skill | Implementation depends on the host / 依赖具体宿主实现 |
| Judgment OS v0.7 | Offline comparison/check/review toolkit + optional prompt Skill / 离线对照、检查、评审工具及可选指导 | No host policy engine or autonomous orchestrator / 未实现宿主策略引擎和自主协调器 |

## Related work / 相关工作

Reviewed repository descriptions and README material on 2026-10-27:

- [SkillsBench](https://github.com/benchflow-ai/skillsbench), Apache-2.0: a benchmark for how agents use Skills. Broader benchmarking is related; no benchmark run or head-to-head comparison was performed here.
- [Skill Eval Harness](https://github.com/adewale/skill-eval-harness), MIT: paired Skill variants, deterministic grading, runner adapters and trace/provenance tooling. There is meaningful overlap; we do not claim paired evaluation or provenance checks are unique.

本次只审阅仓库描述和 README，不是全面竞品测评，不背书对方效果声明。Judgment OS 当前侧重零依赖离线入口、A/B/C/D 小型对照、显式评审轮次与负面结果披露；这些是范围选择，不是性能优势。未复制外部代码或视觉资源，保留原项目 MIT 许可。
