/* ═══════════════════════════════════════════════
   AGRIBOT ENTERPRISE — APP.JS
   ═══════════════════════════════════════════════ */
(function () {
    'use strict';

    // ── STATE ──────────────────────────────────────
    const state = {
        imageFile: null,
        imageBase64: null,
        totalRuns: 0,
        totalLatency: 0,
        confHistory: [],
        currentFilter: 'all',
    };

    // ── ENCYCLOPEDIA DATA ──────────────────────────
    const ENC_DATA = [
        { genus: 'Solanum (Tomato)', condition: 'Early Blight', full: 'Alternaria solani', category: 'Vegetable Foliage', healthy: false, details: 'Concentric ring dark leaf spots causing defoliation. Thrives in warm, wet weather.', treatment: 'Apply copper sulfate or mancozeb fungicide. Remove and destroy infected foliage. Crop rotation advised.' },
        { genus: 'Solanum (Tomato)', condition: 'Late Blight', full: 'Phytophthora infestans', category: 'Vegetable Foliage', healthy: false, details: 'Dark water-soaked lesions with white sporangiophores. Highly contagious oomycete.', treatment: 'Isolate infected plants immediately. Apply metalaxyl-based fungicide. Avoid overhead watering.' },
        { genus: 'Solanum (Tomato)', condition: 'Healthy Seed', full: 'Healthy', category: 'Vegetable Seed', healthy: true, details: 'Optimal seed coat integrity with no pathological markers detected.', treatment: 'Store at 12–15°C and relative humidity below 45%. Use hermetically sealed containers.' },
        { genus: 'Zea (Corn / Maize)', condition: 'Common Rust', full: 'Puccinia sorghi', category: 'Cereal Crop', healthy: false, details: 'Cinnamon-brown pustules on upper and lower leaf surfaces. Wind-dispersed spores.', treatment: 'Apply foliar fungicide (propiconazole or azoxystrobin). Plant resistant hybrids for prevention.' },
        { genus: 'Zea (Corn / Maize)', condition: 'Healthy Seed', full: 'Healthy', category: 'Grain Seed', healthy: true, details: 'Zero rust pustules or lesions detected. Excellent seed vigor index.', treatment: 'Maintain cool, dry storage. Test germination rate before sowing. Monitor for stored grain pests.' },
        { genus: 'Oryza (Rice)', condition: 'Brown Spot', full: 'Bipolaris oryzae', category: 'Cereal Grain', healthy: false, details: 'Oval dark brown lesions with yellow halo on leaf blades, sheaths, and grains.', treatment: 'Apply carbendazim or iprodione. Improve soil nutrition, especially potassium. Avoid waterlogging.' },
        { genus: 'Oryza (Rice)', condition: 'Healthy Seed', full: 'Healthy', category: 'Cereal Grain', healthy: true, details: 'No spotting or lesions detected on leaf tissue or grain surface.', treatment: 'Store in moisture-proof silos. Treat seeds with thiram before planting for fungal prevention.' },
        { genus: 'Triticum (Wheat)', condition: 'Yellow Rust', full: 'Puccinia striiformis', category: 'Cereal Crop', healthy: false, details: 'Yellow stripe pustules aligned in lines along leaf veins. Highly epidemic under cool, moist conditions.', treatment: 'Apply tebuconazole or propiconazole immediately. Plant resistant wheat varieties (e.g., Morocco).' },
        { genus: 'Triticum (Wheat)', condition: 'Healthy Seed', full: 'Healthy', category: 'Cereal Grain', healthy: true, details: 'No rust pustules or pathological markers detected on leaf or grain tissue.', treatment: 'Store at <15°C, <13% moisture content. Inspect for Fusarium infection before sowing.' },
        { genus: 'Glycine (Soybean)', condition: 'Caterpillar Damage', full: 'Spodoptera litura', category: 'Legume Leaf', healthy: false, details: 'Foliar defoliation by tobacco caterpillar larvae leaving skeletonized leaves.', treatment: 'Apply Bt (Bacillus thuringiensis) or spinosad. Use light traps for adult moths. Deep ploughing post-harvest.' },
        { genus: 'Glycine (Soybean)', condition: 'Healthy Seed', full: 'Healthy', category: 'Legume Seed', healthy: true, details: 'No insect damage or pathological lesions detected.', treatment: 'Inoculate with Rhizobium bacteria before planting. Store below 10°C and 12% moisture.' },
        { genus: 'Gossypium (Cotton)', condition: 'Bacterial Blight', full: 'Xanthomonas citri pv. malvacearum', category: 'Fiber Crop', healthy: false, details: 'Angular water-soaked leaf spots with yellow halos. Infects bolls, stems, and leaves.', treatment: 'Use disease-free seed. Spray copper hydroxide. Practice 3-year crop rotation.' },
        { genus: 'Gossypium (Cotton)', condition: 'Healthy Seed', full: 'Healthy', category: 'Fiber Crop', healthy: true, details: 'No bacterial or fungal lesions detected on foliage or fiber bolls.', treatment: 'Acid-delint seeds before planting. Apply thiram seed treatment for fungal prevention.' },
        { genus: 'Helianthus (Sunflower)', condition: 'Powdery Mildew', full: 'Golovinomyces cichoracearum', category: 'Oilseed Crop', healthy: false, details: 'White powdery mycelium coating upper leaf surfaces, reducing photosynthesis.', treatment: 'Apply potassium bicarbonate spray or sulphur-based fungicide. Ensure good canopy airflow.' },
        { genus: 'Helianthus (Sunflower)', condition: 'Healthy Seed', full: 'Healthy', category: 'Oilseed Seed', healthy: true, details: 'No fungal growth or powdery deposits detected on leaf or seed tissue.', treatment: 'Store at <10% moisture and 10°C. Test oil content and germination before trade.' },
    ];

    // ── TELEMETRY CHART ─────────────────────────────
    let confChart = null;
    const confHistCanvas = document.getElementById('confHistChart');
    const chartEmpty = document.getElementById('chartEmpty');

    function initChart() {
        if (!confHistCanvas) return;
        const ctx = confHistCanvas.getContext('2d');
        // Draw empty grid as base (no external library needed)
        drawMiniChart([]);
    }

    function drawMiniChart(data) {
        if (!confHistCanvas) return;
        const canvas = confHistCanvas;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 600;
        const h = 120;
        canvas.width = w; canvas.height = h;

        ctx.clearRect(0, 0, w, h);

        if (data.length < 2) {
            if (chartEmpty) chartEmpty.style.display = 'flex';
            return;
        }
        if (chartEmpty) chartEmpty.style.display = 'none';

        const pad = { top: 10, right: 16, bottom: 24, left: 36 };
        const chartW = w - pad.left - pad.right;
        const chartH = h - pad.top - pad.bottom;

        // Grid lines
        ctx.strokeStyle = 'rgba(255,255,255,0.05)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = pad.top + (chartH / 4) * i;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + chartW, y); ctx.stroke();
            ctx.fillStyle = 'rgba(255,255,255,0.25)';
            ctx.font = '9px JetBrains Mono, monospace';
            ctx.fillText((100 - i * 25) + '%', 2, y + 4);
        }

        // Line & fill
        const pts = data.map((v, i) => ({
            x: pad.left + (i / (data.length - 1)) * chartW,
            y: pad.top + (1 - v / 100) * chartH
        }));

        const grad = ctx.createLinearGradient(0, pad.top, 0, pad.top + chartH);
        grad.addColorStop(0, 'rgba(16,185,129,0.35)');
        grad.addColorStop(1, 'rgba(16,185,129,0)');

        ctx.beginPath();
        ctx.moveTo(pts[0].x, pts[0].y);
        for (let i = 1; i < pts.length; i++) {
            const cp1x = (pts[i - 1].x + pts[i].x) / 2;
            ctx.bezierCurveTo(cp1x, pts[i - 1].y, cp1x, pts[i].y, pts[i].x, pts[i].y);
        }
        ctx.lineTo(pts[pts.length - 1].x, pad.top + chartH);
        ctx.lineTo(pts[0].x, pad.top + chartH);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(pts[0].x, pts[0].y);
        for (let i = 1; i < pts.length; i++) {
            const cp1x = (pts[i - 1].x + pts[i].x) / 2;
            ctx.bezierCurveTo(cp1x, pts[i - 1].y, cp1x, pts[i].y, pts[i].x, pts[i].y);
        }
        ctx.strokeStyle = '#10B981';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Data point dots
        pts.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            ctx.fillStyle = '#10B981';
            ctx.fill();
        });
    }

    // ── LOGGING ────────────────────────────────────
    function log(msg, type = 'ok') {
        const console_ = document.getElementById('sysConsole');
        if (!console_) return;
        const ts = new Date().toLocaleTimeString('en-US', { hour12: false });
        const el = document.createElement('div');
        el.className = `log-entry ${type}`;
        el.innerHTML = `<span class="log-ts">${ts}</span><span>${msg}</span>`;
        console_.appendChild(el);
        console_.scrollTop = console_.scrollHeight;
    }

    // ── API HEALTH CHECK ───────────────────────────
    async function checkHealth() {
        const dot = document.getElementById('statusDot');
        const label = document.getElementById('statusLabel');
        try {
            const res = await fetch('/api/health');
            const data = await res.json();
            if (data.status === 'online') {
                if (dot) dot.classList.add('online');
                if (label) label.textContent = data.model_loaded ? 'Model Active' : 'No Checkpoint';
                log(`Health OK · Model loaded: ${data.model_loaded}`, 'ok');
            }
        } catch {
            if (label) label.textContent = 'Offline';
            log('API unreachable', 'err');
        }
    }

    // ── TAB NAVIGATION ─────────────────────────────
    function initTabs() {
        const tabs = document.querySelectorAll('.tab-btn');
        const pages = document.querySelectorAll('.tab-page');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.tab;
                tabs.forEach(t => t.classList.remove('active'));
                pages.forEach(p => p.classList.add('hidden'));
                tab.classList.add('active');
                const page = document.getElementById('page-' + target);
                if (page) page.classList.remove('hidden');

                // Redraw chart when telemetry tab opens
                if (target === 'telemetry') drawMiniChart(state.confHistory);
            });
        });
    }

    // ── DROPZONE ────────────────────────────────────
    function initDropzone() {
        const dz = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');
        const dzIdle = document.getElementById('dzIdle');
        const dzPreview = document.getElementById('dzPreview');
        const previewImg = document.getElementById('previewImg');
        const clearBtn = document.getElementById('clearBtn');
        const imgBadge = document.getElementById('imgBadge');
        const runBtn = document.getElementById('runBtn');

        if (!dz) return;

        dz.addEventListener('click', (e) => {
            if (!dzPreview.classList.contains('hidden')) return;
            fileInput.click();
        });

        ['dragenter', 'dragover'].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.add('dragover'); }));
        ['dragleave', 'drop'].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.remove('dragover'); }));
        dz.addEventListener('drop', e => {
            const files = e.dataTransfer.files;
            if (files.length) { clearPresets(); loadFile(files[0]); }
        });

        fileInput.addEventListener('change', e => {
            if (e.target.files.length) { clearPresets(); loadFile(e.target.files[0]); }
        });

        clearBtn.addEventListener('click', (e) => {
            e.preventDefault(); e.stopPropagation();
            state.imageFile = null; state.imageBase64 = null;
            fileInput.value = '';
            previewImg.src = '';
            dzIdle.classList.remove('hidden');
            dzPreview.classList.add('hidden');
            if (runBtn) runBtn.disabled = true;
            clearPresets();
            showEmpty();
            clearAttentionMap();
            log('Sample cleared', 'ok');
        });

        function loadFile(file) {
            if (!file.type.startsWith('image/')) return alert('Please select an image file.');
            state.imageFile = file;
            state.imageBase64 = null;
            const reader = new FileReader();
            reader.onload = e => {
                previewImg.src = e.target.result;
                dzIdle.classList.add('hidden');
                dzPreview.classList.remove('hidden');
                if (imgBadge) imgBadge.textContent = file.name;
                if (runBtn) runBtn.disabled = false;
                log(`Loaded file: ${file.name}`, 'ok');
                if (document.getElementById('attentionToggle')?.checked) drawAttentionMap();
            };
            reader.readAsDataURL(file);
        }
    }

    // ── ATTENTION MAP ───────────────────────────────
    function drawAttentionMap() {
        const canvas = document.getElementById('attentionCanvas');
        const img = document.getElementById('previewImg');
        if (!canvas || !img || !img.src) return;

        canvas.classList.remove('hidden');
        const rect = img.getBoundingClientRect();
        canvas.width = img.naturalWidth || 128;
        canvas.height = img.naturalHeight || 128;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Simulated attention hotspot (center-biased radial gradient)
        const cx = canvas.width * 0.5, cy = canvas.height * 0.45;
        const grad = ctx.createRadialGradient(cx, cy, 5, cx, cy, canvas.width * 0.6);
        grad.addColorStop(0, 'rgba(239, 68, 68, 0.75)');
        grad.addColorStop(0.4, 'rgba(245, 158, 11, 0.45)');
        grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function clearAttentionMap() {
        const canvas = document.getElementById('attentionCanvas');
        if (canvas) canvas.classList.add('hidden');
    }

    // ── SETTINGS CONTROLS ────────────────────────────
    function initSettings() {
        const slider = document.getElementById('threshSlider');
        const label = document.getElementById('threshLabel');
        if (slider) {
            const updateFill = () => {
                const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
                slider.style.background = `linear-gradient(90deg, #10B981 ${pct}%, rgba(255,255,255,0.1) ${pct}%)`;
                if (label) label.textContent = slider.value + '%';
                log(`Sensitivity threshold → ${slider.value}%`, 'ok');
            };
            slider.addEventListener('input', updateFill);
            updateFill();
        }

        const attToggle = document.getElementById('attentionToggle');
        if (attToggle) {
            attToggle.addEventListener('change', () => {
                if (attToggle.checked) {
                    drawAttentionMap();
                    log('Attention map overlay: ON', 'ok');
                } else {
                    clearAttentionMap();
                    log('Attention map overlay: OFF', 'ok');
                }
            });
        }
    }

    // ── PRESETS ──────────────────────────────────────
    function clearPresets() {
        document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
    }

    function initPresets() {
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                clearPresets();
                btn.classList.add('active');
                log(`Preset selected: ${btn.querySelector('.preset-name').textContent}`, 'ok');
                fetchRandomSample();
            });
        });
    }

    // ── SAMPLE FETCH ────────────────────────────────
    async function fetchRandomSample() {
        const sampleBtn = document.getElementById('sampleBtn');
        if (sampleBtn) { sampleBtn.disabled = true; sampleBtn.textContent = 'Loading...'; }

        try {
            const res = await fetch('/api/sample');
            const data = await res.json();

            if (data.success) {
                state.imageBase64 = data.image_base64;
                state.imageFile = null;

                const previewImg = document.getElementById('previewImg');
                const dzIdle = document.getElementById('dzIdle');
                const dzPreview = document.getElementById('dzPreview');
                const imgBadge = document.getElementById('imgBadge');
                const runBtn = document.getElementById('runBtn');

                if (previewImg) previewImg.src = data.image_base64;
                if (dzIdle) dzIdle.classList.add('hidden');
                if (dzPreview) dzPreview.classList.remove('hidden');
                if (imgBadge) imgBadge.textContent = data.sample_class.replace(/_/g, ' ');
                if (runBtn) runBtn.disabled = false;

                if (document.getElementById('attentionToggle')?.checked) drawAttentionMap();
                log(`Sample loaded: ${data.sample_class}`, 'ok');
                runAnalysis();
            } else {
                log('Sample fetch failed: ' + data.error, 'err');
            }
        } catch (e) {
            log('Network error fetching sample: ' + e.message, 'err');
        } finally {
            if (sampleBtn) {
                sampleBtn.disabled = false;
                sampleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z" stroke="currentColor" stroke-width="1.5"/></svg> Random Sample`;
            }
        }
    }

    // ── RUN ANALYSIS ─────────────────────────────────
    async function runAnalysis() {
        const runBtn = document.getElementById('runBtn');
        const emptyState = document.getElementById('emptyState');
        const loadingState = document.getElementById('loadingState');
        const resultsPanel = document.getElementById('resultsPanel');

        if (emptyState) emptyState.classList.add('hidden');
        if (resultsPanel) resultsPanel.classList.add('hidden');
        if (loadingState) loadingState.classList.remove('hidden');

        // Animate loading steps
        const steps = ['lstep1', 'lstep2', 'lstep3'];
        steps.forEach((id, i) => {
            const el = document.getElementById(id);
            if (el) { el.classList.remove('active'); setTimeout(() => el.classList.add('active'), i * 400); }
        });

        if (runBtn) {
            runBtn.disabled = true;
            runBtn.querySelector('.btn-inner')?.classList.add('hidden');
            runBtn.querySelector('.btn-loading')?.classList.remove('hidden');
        }

        const start = performance.now();

        try {
            let res;
            if (state.imageFile) {
                const fd = new FormData();
                fd.append('image', state.imageFile);
                res = await fetch('/api/predict', { method: 'POST', body: fd });
            } else if (state.imageBase64) {
                res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image_base64: state.imageBase64 })
                });
            } else { return; }

            const data = await res.json();
            const latency = Math.round(performance.now() - start);

            if (loadingState) loadingState.classList.add('hidden');

            if (data.success) {
                state.totalRuns++;
                state.totalLatency += latency;
                state.confHistory.push(Number(data.confidence_percentage) || 0);
                if (state.confHistory.length > 20) state.confHistory.shift();

                updateTelemetry(latency);
                renderResults(data);
                log(`Inference #${state.totalRuns} in ${latency}ms · ${data.class_name} (${(Number(data.confidence_percentage)||0).toFixed(1)}%)`, 'ok');
            } else {
                log('Prediction error: ' + data.error, 'err');
                showEmpty();
            }
        } catch (e) {
            if (loadingState) loadingState.classList.add('hidden');
            log('Network error: ' + e.message, 'err');
            showEmpty();
        } finally {
            if (runBtn) {
                runBtn.disabled = false;
                runBtn.querySelector('.btn-inner')?.classList.remove('hidden');
                runBtn.querySelector('.btn-loading')?.classList.add('hidden');
            }
        }
    }

    function updateTelemetry(latency) {
        const avgEl = document.getElementById('avgLatency');
        const runsEl = document.getElementById('totalRuns');
        if (avgEl) avgEl.textContent = Math.round(state.totalLatency / state.totalRuns);
        if (runsEl) runsEl.textContent = state.totalRuns;
        drawMiniChart(state.confHistory);
    }

    // ── RENDER RESULTS ────────────────────────────────
    function renderResults(data) {
        const resultsPanel = document.getElementById('resultsPanel');
        if (!resultsPanel) return;
        resultsPanel.classList.remove('hidden');

        // Verification stripe
        const stripe = document.getElementById('verifyStripe');
        const vIcon = document.getElementById('verifyIcon');
        const vText = document.getElementById('verifyText');
        if (stripe) {
            if (data.is_plant) {
                stripe.classList.remove('invalid');
                if (vIcon) vIcon.textContent = '✓';
                if (vText) vText.textContent = `Valid Plant Sample Verified · ${data.plant_verification_message || ''}`;
            } else {
                stripe.classList.add('invalid');
                if (vIcon) vIcon.textContent = '⚠';
                if (vText) vText.textContent = `Non-Plant / Out-of-Domain · ${data.plant_verification_message || ''}`;
            }
        }

        // Diagnosis card
        const cropLabel = document.getElementById('cropLabel');
        const genusName = document.getElementById('genusName');
        const healthBadge = document.getElementById('healthBadge');
        const condVal = document.getElementById('condVal');
        if (cropLabel) cropLabel.textContent = data.crop_type || 'AGRICULTURAL CROP';
        if (genusName) genusName.textContent = data.genus || 'Unknown Genus';
        if (condVal) condVal.textContent = data.disease || 'Unknown';
        if (healthBadge) {
            healthBadge.textContent = data.is_healthy ? 'Healthy' : 'Disease Detected';
            healthBadge.className = 'health-badge ' + (data.is_healthy ? 'healthy' : 'diseased');
        }

        // Confidence meter
        const conf = (Number(data.confidence_percentage) || 0).toFixed(2);
        const confPct = document.getElementById('confPct');
        const confFill = document.getElementById('confFill');
        const qualityLabel = document.getElementById('qualityLabel');
        if (confPct) confPct.textContent = conf + '%';
        if (confFill) setTimeout(() => confFill.style.width = conf + '%', 80);
        if (qualityLabel) {
            const c = Number(conf);
            qualityLabel.textContent = c >= 80 ? 'High Confidence' : c >= 50 ? 'Moderate Confidence' : 'Low Confidence — consider re-imaging';
            qualityLabel.style.color = c >= 80 ? '#10B981' : c >= 50 ? '#F59E0B' : '#EF4444';
        }

        // Candidates
        const list = document.getElementById('candidatesList');
        if (list && data.top3) {
            list.innerHTML = '';
            data.top3.forEach(item => {
                const row = document.createElement('div');
                row.className = 'candidate-row';
                const p = (Number(item.confidence) || 0).toFixed(2);
                row.innerHTML = `<span class="cand-name">${item.genus || item.class_name} <small>(${item.class_name})</small></span><span class="cand-pct">${p}%</span>`;
                list.appendChild(row);
            });
        }

        // Recommendations
        const recsList = document.getElementById('recsList');
        if (recsList && data.recommendations) {
            recsList.innerHTML = '';
            data.recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recsList.appendChild(li);
            });
        }
    }

    function showEmpty() {
        const emptyState = document.getElementById('emptyState');
        const resultsPanel = document.getElementById('resultsPanel');
        if (emptyState) emptyState.classList.remove('hidden');
        if (resultsPanel) resultsPanel.classList.add('hidden');
    }

    // ── ENCYCLOPEDIA ──────────────────────────────────
    function renderEncyclopedia(data) {
        const grid = document.getElementById('encGrid');
        if (!grid) return;
        grid.innerHTML = '';

        if (!data.length) {
            grid.innerHTML = '<div style="color:var(--c-text-3);padding:40px;text-align:center;font-size:13px;">No results found for that query.</div>';
            return;
        }

        data.forEach((item, idx) => {
            const card = document.createElement('div');
            card.className = 'enc-card';
            card.style.animationDelay = (idx * 30) + 'ms';
            card.innerHTML = `
                <div class="enc-card-top">
                    <span class="enc-cat">${item.category}</span>
                    <span class="enc-badge ${item.healthy ? 'h' : 'd'}">${item.healthy ? 'Healthy' : 'Diseased'}</span>
                </div>
                <div class="enc-genus">${item.genus}</div>
                <div class="enc-cond">${item.condition}</div>
            `;
            card.addEventListener('click', () => openModal(item));
            grid.appendChild(card);
        });
    }

    function filterEnc() {
        const q = (document.getElementById('encSearch')?.value || '').toLowerCase();
        return ENC_DATA.filter(item => {
            const matchText = item.genus.toLowerCase().includes(q) || item.condition.toLowerCase().includes(q) || item.category.toLowerCase().includes(q);
            const matchFilter = state.currentFilter === 'all' ||
                (state.currentFilter === 'healthy' && item.healthy) ||
                (state.currentFilter === 'disease' && !item.healthy);
            return matchText && matchFilter;
        });
    }

    function initEncyclopedia() {
        renderEncyclopedia(ENC_DATA);

        const search = document.getElementById('encSearch');
        if (search) search.addEventListener('input', () => renderEncyclopedia(filterEnc()));

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.currentFilter = btn.dataset.filter;
                renderEncyclopedia(filterEnc());
            });
        });
    }

    // ── MODAL ─────────────────────────────────────────
    function openModal(item) {
        const modal = document.getElementById('modal');
        const tag = document.getElementById('modalTag');
        const title = document.getElementById('modalTitle');
        const content = document.getElementById('modalContent');
        if (!modal) return;

        if (tag) tag.textContent = item.category;
        if (title) title.textContent = item.genus;
        if (content) {
            content.innerHTML = `
                <div class="modal-row"><div class="modal-key">Pathological Condition</div><div class="modal-val" style="color:var(--c-amber)">${item.condition}</div></div>
                <div class="modal-row"><div class="modal-key">Pathogen / Cause</div><div class="modal-val" style="font-style:italic">${item.full}</div></div>
                <div class="modal-row"><div class="modal-key">Status</div><div class="modal-val"><span class="enc-badge ${item.healthy ? 'h' : 'd'}">${item.healthy ? 'Healthy — No Disease' : 'Disease Detected'}</span></div></div>
                <div class="modal-divider"></div>
                <div class="modal-row"><div class="modal-key">Description</div><div class="modal-val">${item.details}</div></div>
                <div class="modal-row"><div class="modal-key">Treatment & Action Protocol</div><div class="modal-val" style="color:#A7F3D0">${item.treatment}</div></div>
            `;
        }
        modal.classList.remove('hidden');
    }

    function initModal() {
        const modal = document.getElementById('modal');
        const closeBtn = document.getElementById('modalClose');
        if (closeBtn) closeBtn.addEventListener('click', () => modal?.classList.add('hidden'));
        if (modal) modal.addEventListener('click', e => { if (e.target === modal) modal.classList.add('hidden'); });
        document.addEventListener('keydown', e => { if (e.key === 'Escape') modal?.classList.add('hidden'); });
    }

    // ── CONSOLE CLEAR ─────────────────────────────────
    document.getElementById('clearConsole')?.addEventListener('click', () => {
        const c = document.getElementById('sysConsole');
        if (c) c.innerHTML = '';
    });

    // ── RUN BTN ───────────────────────────────────────
    document.getElementById('runBtn')?.addEventListener('click', runAnalysis);
    document.getElementById('sampleBtn')?.addEventListener('click', () => { clearPresets(); fetchRandomSample(); });

    // ── INIT ──────────────────────────────────────────
    initTabs();
    initDropzone();
    initSettings();
    initPresets();
    initEncyclopedia();
    initModal();
    initChart();
    checkHealth();
})();
