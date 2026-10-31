# Guardrail rescoring: eval_20261030T231525Z_tune_small_v2

Run log: runs/eval_20261030T231525Z_tune_small_v2.jsonl (not modified). Records: 56. No API calls. Old = counts logged at run time. New = current src/guardrails.py on customer facing text only.

Totals: old violations 10, new violations 7, new warnings 12.

| Case | Mode | Version | Text checked | Old violations | Old hits | New violations | New hits | New warnings | Warning hits |
|---|---|---|---|---|---|---|---|---|---|
| CS-5203 | fields_only | v2 | draft_reply | 1 | promises_action: We will review your refund | 0 | - | 0 | - |
| CS-5203 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5204 | fields_only | v2 | draft_reply | 1 | promises_action: We'll arrange an exchange, we'll ship | 1 | promises_action: We'll arrange an exchange, we'll ship | 0 | - |
| CS-5204 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5205 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5205 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5206 | fields_only | v2 | draft_reply | 0 | stop_use_advice: stop using | 0 | - | 1 | stop_use_advice: stop using |
| CS-5206 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5210 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5210 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5213 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5213 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5218 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5218 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5219 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5219 | fields_plus_simulated_message | v2 | draft_reply | 1 | promises_action: we'll refund | 1 | promises_action: we'll refund | 0 | - |
| CS-5220 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5220 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5221 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5221 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5222 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5222 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5223 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5223 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5224 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5224 | fields_plus_simulated_message | v2 | draft_reply | 1 | reveals_fraud_criteria: Fraud | 1 | reveals_fraud_criteria: Fraud | 0 | - |
| CS-5225 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5225 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5227 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5227 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5229 | fields_only | v2 | draft_reply | 0 | stop_use_advice: stop using; unsourced_safety_instruction: do not cut, seek medical attention | 0 | - | 2 | stop_use_advice: stop using; unsourced_safety_instruction: do not cut, seek medical attention |
| CS-5229 | fields_plus_simulated_message | v2 | draft_reply | 0 | stop_use_advice: stop using; unsourced_safety_instruction: Do not cut | 0 | - | 2 | stop_use_advice: stop using; unsourced_safety_instruction: Do not cut |
| CS-5233 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5233 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5235 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5235 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5236 | fields_only | v2 | draft_reply | 0 | stop_use_advice: stop using; unsourced_safety_instruction: do not cut | 0 | - | 2 | stop_use_advice: stop using; unsourced_safety_instruction: do not cut |
| CS-5236 | fields_plus_simulated_message | v2 | draft_reply | 2 | promises_action: is covered under warranty; safety_clearance: safe to use; stop_use_advice: stop using, do not climb | 2 | promises_action: is covered under warranty; safety_clearance: safe to use | 1 | stop_use_advice: stop using, do not climb |
| CS-5239 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5239 | fields_plus_simulated_message | v2 | draft_reply | 1 | promises_action: Your refund will be processed | 1 | promises_action: Your refund will be processed | 0 | - |
| CS-5241 | fields_only | v2 | draft_reply | 0 | stop_use_advice: do not use | 0 | - | 1 | stop_use_advice: do not use |
| CS-5241 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5242 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5242 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5243 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5243 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5244 | fields_only | v2 | draft_reply | 1 | promises_action: We've received your refund | 0 | - | 0 | - |
| CS-5244 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5245 | fields_only | v2 | draft_reply | 1 | inspection_or_repair_advice: check your carabiner; stop_use_advice: stop using | 1 | inspection_or_repair_advice: check your carabiner | 1 | stop_use_advice: stop using |
| CS-5245 | fields_plus_simulated_message | v2 | draft_reply | 0 | stop_use_advice: do not use | 0 | - | 1 | stop_use_advice: do not use |
| CS-5246 | fields_only | v2 | draft_reply | 0 | stop_use_advice: stop using | 0 | - | 1 | stop_use_advice: stop using |
| CS-5246 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5247 | fields_only | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5247 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
| CS-5248 | fields_only | v2 | draft_reply | 1 | promises_action: We have received your refund | 0 | - | 0 | - |
| CS-5248 | fields_plus_simulated_message | v2 | draft_reply | 0 | - | 0 | - | 0 | - |
