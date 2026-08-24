(function () {
    'use strict';

    const workspace = document.getElementById('coding-workspace');
    if (!workspace) return;

    const questionId = workspace.dataset.questionId;
    const csrfToken = workspace.dataset.csrf;
    const timerActive = workspace.dataset.timerActive === 'true';
    const expiresMs = parseInt(workspace.dataset.expiresMs, 10);
    const serverNowMs = parseInt(workspace.dataset.serverNowMs, 10);

    const starterCodesEl = document.getElementById('starter-codes');
    const starterCodes = starterCodesEl ? JSON.parse(starterCodesEl.textContent) : {};

    const LANG_MONACO = {
        python: 'python',
        java: 'java',
        javascript: 'javascript',
        cpp: 'cpp',
        c: 'c',
    };

    const STORAGE_KEY = `codeeval_q${questionId}`;

    let editor = null;
    let currentLanguage = 'python';
    let timerExpired = false;

    function getSavedState() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        } catch {
            return {};
        }
    }

    function saveState() {
        if (!editor) return;
        const state = getSavedState();
        state[currentLanguage] = editor.getValue();
        state.lastLanguage = currentLanguage;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function loadLanguageCode(lang) {
        const saved = getSavedState();
        if (saved[lang]) return saved[lang];
        return starterCodes[lang] || starterCodes.python || '';
    }

    function initTimer() {
        if (!timerActive || !expiresMs) return;

        const display = document.getElementById('timer-display');
        const timerEl = document.getElementById('coding-timer');
        const offset = Date.now() - serverNowMs;

        function tick() {
            const now = Date.now() - offset;
            const remaining = Math.max(0, expiresMs - now);
            const mins = Math.floor(remaining / 60000);
            const secs = Math.floor((remaining % 60000) / 1000);
            if (display) {
                display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
            }
            if (remaining <= 0) {
                timerExpired = true;
                if (timerEl) timerEl.classList.add('expired');
                if (display) display.textContent = 'EXPIRED';
                disableActions();
                setStatus('Timed assessment expired');
                clearInterval(interval);
            }
        }

        tick();
        const interval = setInterval(tick, 1000);
    }

    function disableActions() {
        const runBtn = document.getElementById('run-btn');
        const submitBtn = document.getElementById('submit-btn');
        if (runBtn) runBtn.disabled = true;
        if (submitBtn) submitBtn.disabled = true;
    }

    function setStatus(text) {
        const el = document.getElementById('execution-status');
        if (el) el.textContent = text;
    }

    function setMessage(text) {
        const el = document.getElementById('results-message');
        if (el) el.textContent = text;
    }

    function renderTestResults(results) {
        const container = document.getElementById('test-results');
        if (!container) return;
        container.innerHTML = '';

        results.forEach((r, i) => {
            const item = document.createElement('div');
            let cls = 'pending';
            let icon = '⏳';
            if (r.passed === true) { cls = 'passed'; icon = '✓'; }
            else if (r.passed === false) { cls = 'failed'; icon = '✗'; }
            else if (r.status === 'not_executed') { cls = 'pending'; icon = '○'; }

            item.className = `test-result-item ${cls}`;
            item.innerHTML = `
                <div class="test-result-header">
                    <span>Test Case ${i + 1}${r.is_sample ? ' (Sample)' : ''}</span>
                    <span>${icon} ${r.passed === true ? 'Passed' : r.passed === false ? 'Failed' : 'Not Executed'}</span>
                </div>
                <div class="test-result-detail">
                    <div><strong>Input</strong><pre>${escapeHtml(r.input_data)}</pre></div>
                    <div><strong>Expected Output</strong><pre>${escapeHtml(r.expected_output)}</pre></div>
                    ${r.actual_output != null ? `<div><strong>Actual Output</strong><pre>${escapeHtml(r.actual_output)}</pre></div>` : ''}
                    ${r.error ? `<div><strong>Error</strong><pre>${escapeHtml(r.error)}</pre></div>` : ''}
                </div>
            `;
            container.appendChild(item);
        });
    }

    function escapeHtml(str) {
        if (str == null) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    async function apiCall(endpoint, code, language) {
        const resp = await fetch(`/api/coding/${questionId}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
            },
            body: JSON.stringify({ code, language }),
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'Request failed');
        return data;
    }

    async function runCode() {
        if (timerExpired) return;
        saveState();
        const code = editor.getValue();
        const runBtn = document.getElementById('run-btn');
        runBtn.disabled = true;
        setStatus('Running...');
        setMessage('');

        try {
            const data = await apiCall('run', code, currentLanguage);
            setStatus(data.status || 'Done');
            setMessage(data.message || '');
            renderTestResults(data.test_results || []);
        } catch (err) {
            setStatus('Error');
            setMessage(err.message);
        } finally {
            runBtn.disabled = timerExpired;
        }
    }

    async function submitCode() {
        if (timerExpired) return;
        saveState();
        const code = editor.getValue();
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.disabled = true;
        setStatus('Submitting...');

        try {
            const data = await apiCall('submit', code, currentLanguage);
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } catch (err) {
            setStatus('Error');
            setMessage(err.message);
            submitBtn.disabled = timerExpired;
        }
    }

    function switchLanguage(lang) {
        saveState();
        currentLanguage = lang;
        const monacoLang = LANG_MONACO[lang] || 'python';
        if (editor) {
            editor.setValue(loadLanguageCode(lang));
            monaco.editor.setModelLanguage(editor.getModel(), monacoLang);
        }
    }

    function initMonaco() {
        require.config({
            paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' },
        });

        require(['vs/editor/editor.main'], function () {
            const saved = getSavedState();
            currentLanguage = saved.lastLanguage || 'python';

            const langSelect = document.getElementById('language-select');
            if (langSelect) langSelect.value = currentLanguage;

            editor = monaco.editor.create(document.getElementById('monaco-editor'), {
                value: loadLanguageCode(currentLanguage),
                language: LANG_MONACO[currentLanguage] || 'python',
                theme: 'vs-dark',
                fontSize: 14,
                fontFamily: "'Consolas', 'Courier New', monospace",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                insertSpaces: true,
                wordWrap: 'on',
            });

            editor.onDidChangeModelContent(() => {
                clearTimeout(window._codeSaveTimer);
                window._codeSaveTimer = setTimeout(saveState, 500);
            });

            document.getElementById('run-btn')?.addEventListener('click', runCode);
            document.getElementById('submit-btn')?.addEventListener('click', submitCode);

            langSelect?.addEventListener('change', (e) => {
                switchLanguage(e.target.value);
            });

            initTimer();
        });
    }

    initMonaco();
})();
