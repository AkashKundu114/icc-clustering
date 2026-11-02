Created At: 2026-11-01T21:31:17+05:30
Completed At: 2026-11-01T21:31:18+05:30
File Path: `file:///d:/icc-clustering/src/icc/consensus/autok.py`
Total Lines: 231
Total Bytes: 8090
Showing lines 151 to 231
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
151: 
152:     for idx, k in enumerate(candidate_ks):
153:         model = InvariantCoreConsensusV2(
154:             n_clusters=k,
155:             n_base_models=n_base_models,
156:             n_anchors=n_anchors,
157:             subspace_rate=subspace_rate,
158:             pool_frac=pool_frac,
159:             random_state=seed + idx,
160:         )
161:         labels = model.fit_predict(X_arr)
162:         all_labels[k] = labels
163: 
164:         # Authentic bipartite anchor co-occurrence projection B in R^(N x L)
165:         b_norm = getattr(model, "B_norm_", None)
166:         if b_norm is not None and getattr(b_norm, "shape", (0,))[0] == N:
167:             pac, area = compute_anchor_pac(b_norm, n_pairs=n_pairs, random_state=seed)
168:         elif model.U_emb_ is not None and model.U_emb_.shape[0] == N:
169:             U = model.U_emb_
170:             U_norm = U / (np.linalg.norm(U, axis=1, keepdims=True) + 1e-12)
171:             pac, area = compute_anchor_pac(U_norm, n_pairs=n_pairs, random_state=seed)
172:         else:
173:             # Fallback to one-hot assignment co-association
174:             one_hot = np.zeros((N, k), dtype=np.float64)
175:             one_hot[np.arange(N), labels] = 1.0
176:             pac, area = compute_anchor_pac(one_hot, n_pairs=n_pairs, random_state=seed)
177: 
178:         pac_scores[k] = pac
179:         cdf_areas[k] = area
180: 
181:         if idx == 0:
182:             delta_areas[k] = area
183:         else:
184:             delta_areas[k] = (area - prev_area) / max(prev_area, 1e-6)
185
<truncated 274 bytes>
r silhouette if N > 2000 for compute efficiency
192:                 if N > 2000:
193:                     sub_idx = np.random.default_rng(seed).choice(N, size=2000, replace=False)
194:                     silhouette_scores[k] = float(silhouette_score(X_arr[sub_idx], labels[sub_idx]))
195:                 else:
196:                     silhouette_scores[k] = float(silhouette_score(X_arr, labels))
197:                 ch_scores[k] = float(calinski_harabasz_score(X_arr, labels))
198:                 db_scores[k] = float(davies_bouldin_score(X_arr, labels))
199:             except Exception:
200:                 silhouette_scores[k] = -1.0
201:                 ch_scores[k] = 0.0
202:                 db_scores[k] = 999.0
203:         else:
204:             silhouette_scores[k] = -1.0
205:             ch_scores[k] = 0.0
206:             db_scores[k] = 999.0
207: 
208:     # Model selection decision rule: minimum PAC with Occam's parsimony tolerance (+0.02)
209:     _min_pac = min(pac_scores.values())  # noqa: F841
210:     best_k_pac = min(pac_scores.keys(), key=lambda k: pac_scores[k])
211: 
212:     # Secondary decision rule: maximum Silhouette
213:     best_k_sil = max(silhouette_scores.keys(), key=lambda k: silhouette_scores[k])
214: 
215:     runtime_sec = time.perf_counter() - t0
216: 
217:     return AutoKResult(
218:         best_k_pac=best_k_pac,
219:         best_k_silhouette=best_k_sil,
220:         best_labels_pac=all_labels[best_k_pac],
221:         best_labels_silhouette=all_labels[best_k_sil],
222:         candidate_ks=candidate_ks,
223:         pac_scores=pac_scores,
224:         silhouette_scores=silhouette_scores,
225:         ch_scores=ch_scores,
226:         db_scores=db_scores,
227:         delta_areas=delta_areas,
228:         runtime_sec=runtime_sec,
229:     )
230: 
231: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
