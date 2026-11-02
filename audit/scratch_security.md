Created At: 2026-11-01T21:31:19+05:30
Completed At: 2026-11-01T21:31:20+05:30
File Path: `file:///d:/icc-clustering/configs/datasets.yaml`
Total Lines: 282
Total Bytes: 7524
Showing lines 101 to 282
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
101:     name: "cns"
102:     domain: "genomics"
103:     source: "openml"
104:     openml_id: 45086
105:     openml_name: "cns"
106:     openml_version: 1
107:     expected_N: 60
108:     expected_D: 7129
109:     expected_K: 2
110:     d_over_n_ratio: 118.82
111:     preprocessing:
112:       standardize: true
113:       impute_nan: true
114:       log_transform: false
115:       hvg_filter: false
116:     priority: "critical"
117:     enabled: true
118:     description: "Central Nervous System embryonal tumors (survivors vs fatalities)"
119: 
120:   leukemia:
121:     name: "leukemia"
122:     domain: "genomics"
123:     source: "openml"
124:     openml_id: 1104
125:     openml_name: "leukemia"
126:     openml_version: 1
127:     expected_N: 72
128:     expected_D: 7129
129:     expected_K: 2
130:     d_over_n_ratio: 99.01
131:     preprocessing:
132:       standardize: true
133:       impute_nan: true
134:       log_transform: false
135:       hvg_filter: false
136:     priority: "critical"
137:     enabled: true
138:     description: "Golub et al. acute leukemia microarray (ALL vs AML)"
139: 
140:   prostate:
141:     name: "prostate"
142:     domain: "genomics"
143:     source: "openml"
144:     openml_id: 45099
145:     openml_name: "prostate"
146:     openml_version: 1
147:     expected_N: 102
148:     expected_D: 12600
149:     expected_K: 2
150:     d_over_n_ratio: 123.53
151:     preprocessing:
152:       standardize: true
153:       impute_nan: true
154:       log_transform: false
155:       hvg_filter: false
156: 
<truncated 2318 bytes>
"url"
227:     openml_id: null
228:     loader: "spectral.load_indian_pines"
229:     url: "https://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat"
230:     expected_N: 10249
231:     expected_D: 200
232:     expected_K: 16
233:     d_over_n_ratio: 0.02
234:     preprocessing:
235:       standardize: true
236:       impute_nan: false
237:       log_transform: false
238:       hvg_filter: false
239:     priority: "high"
240:     enabled: true
241:     description: "Indian Pines hyperspectral imaging flight line over NW Indiana (N=10249, D=200, K=16)"
242: 
243:   yale_b:
244:     name: "yale_b"
245:     domain: "image"
246:     source: "url"
247:     openml_id: null
248:     loader: "image.load_yale_b"
249:     url: "http://vision.ucsd.edu/extyaleb/CroppedYaleB.zip"
250:     expected_N: 2414
251:     expected_D: 1024
252:     expected_K: 38
253:     d_over_n_ratio: 0.42
254:     preprocessing:
255:       standardize: true
256:       impute_nan: false
257:       log_transform: false
258:       hvg_filter: false
259:     priority: "high"
260:     enabled: true
261:     description: "Extended Yale B cropped face images with varying illumination angles (N=2414, D=1024, K=38)"
262: 
263:   zheng68k:
264:     name: "zheng68k"
265:     domain: "scrnaseq"
266:     source: "scanpy"
267:     openml_id: null
268:     loader: "scrnaseq.load_zheng68k"
269:     expected_N: 700
270:     expected_D: 765
271:     expected_K: 10
272:     d_over_n_ratio: 1.09
273:     preprocessing:
274:       standardize: true
275:       impute_nan: false
276:       log_transform: true
277:       hvg_filter: true
278:     priority: "critical"
279:     enabled: true
280:     description: "Zheng et al. 2017 PBMC scRNA-seq profiling (reduced subset: N=700, D=765, K=10, extreme sparsity)"
281: 
282: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
