document.addEventListener("DOMContentLoaded", () => {
    const f1Input = document.getElementById("fighter1");
    const f2Input = document.getElementById("fighter2");
    const ac1 = document.getElementById("autocomplete1");
    const ac2 = document.getElementById("autocomplete2");

    let allFighters = [];

    // Fetch fighters + update hero stat
    fetch("/api/fighters")
        .then(res => res.json())
        .then(data => {
            allFighters = data.fighters || [];
            const countEl = document.getElementById("fighter-count");
            if (countEl) countEl.textContent = allFighters.length.toLocaleString();
        })
        .catch(err => console.error(err));

    // ---- Autocomplete ----
    function setupAutocomplete(inputEl, listEl) {
        inputEl.addEventListener("input", function () {
            const val = this.value;
            listEl.innerHTML = "";
            if (!val) {
                listEl.classList.add("hidden");
                return;
            }
            const matches = allFighters.filter(f => f.toLowerCase().includes(val.toLowerCase())).slice(0, 10);
            if (matches.length > 0) {
                listEl.classList.remove("hidden");
                matches.forEach(match => {
                    const li = document.createElement("li");
                    const regex = new RegExp(`(${val.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, "gi");
                    li.innerHTML = match.replace(regex, "<strong>$1</strong>");
                    li.addEventListener("click", () => {
                        inputEl.value = match;
                        listEl.innerHTML = "";
                        listEl.classList.add("hidden");
                    });
                    listEl.appendChild(li);
                });
            } else {
                listEl.classList.add("hidden");
            }
        });

        document.addEventListener("click", function (e) {
            if (e.target !== inputEl && e.target !== listEl) {
                listEl.classList.add("hidden");
            }
        });
    }

    setupAutocomplete(f1Input, ac1);
    setupAutocomplete(f2Input, ac2);

    // ---- Active nav link tracking ----
    const navLinks = document.querySelectorAll('.nav-link[data-section]');
    const sections = document.querySelectorAll('.hero, .section, .result-section');

    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id || entry.target.querySelector('[id]')?.id;
                navLinks.forEach(link => {
                    const match = link.getAttribute('data-section');
                    if (match === id || (id === 'hero' && match === 'predict')) {
                        link.classList.add('active');
                    } else if (match === 'results' && id === 'result-section') {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(sec => navObserver.observe(sec));

    // ---- Scroll reveal ----
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // ---- Prediction ----
    const matchBtn = document.getElementById("predict-btn");
    const btnText = document.querySelector(".btn-text");
    const loader = document.querySelector(".loader");
    const resultSec = document.getElementById("result-section");

    matchBtn.addEventListener("click", () => {
        const fighter1 = f1Input.value.trim();
        const fighter2 = f2Input.value.trim();

        if (!fighter1 || !fighter2) {
            alert("Please select both fighters.");
            return;
        }

        resultSec.classList.add("hidden");
        btnText.classList.add("hidden");
        loader.classList.remove("hidden");
        matchBtn.disabled = true;

        fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fighter1, fighter2 })
        })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    renderResults(data);
                }
            })
            .catch(err => {
                console.error(err);
                alert("Network error.");
            })
            .finally(() => {
                btnText.classList.remove("hidden");
                loader.classList.add("hidden");
                matchBtn.disabled = false;
            });
    });

    function fmt(val, suffix) {
        if (val === null || val === undefined) return "\u2014";
        return suffix ? val + suffix : String(val);
    }

    function renderResults(data) {
        const { fighter1, fighter2, winner, f1Prob, f2Prob, f1, f2 } = data;
        const p1 = (f1Prob * 100).toFixed(1);
        const p2 = (f2Prob * 100).toFixed(1);

        // Probability bar
        document.getElementById("prob-f1-name").textContent = fighter1;
        document.getElementById("prob-f2-name").textContent = fighter2;
        document.getElementById("prob-f1-val").textContent = p1 + "%";
        document.getElementById("prob-f2-val").textContent = p2 + "%";

        const f1Fill = document.getElementById("prob-f1-fill");
        const f2Fill = document.getElementById("prob-f2-fill");
        f1Fill.style.width = "0%";
        f2Fill.style.width = "0%";

        // Winner indicator
        document.getElementById("winner-name").textContent = winner;
        const arrowL = document.getElementById("winner-arrow");
        const arrowR = document.getElementById("winner-arrow-r");
        arrowL.classList.toggle("active", winner === fighter1);
        arrowR.classList.toggle("active", winner === fighter2);

        // Activate results nav link
        const navResults = document.getElementById("nav-results");
        if (navResults) navResults.classList.add("active");

        // Fighter profiles
        renderProfile("f1", fighter1, f1);
        renderProfile("f2", fighter2, f2);

        // Comparison bars
        renderComparison(fighter1, fighter2, f1, f2);

        // Win method breakdown
        renderMethods(f1, f2);

        // Show results then animate bars
        resultSec.classList.remove("hidden");

        setTimeout(() => {
            f1Fill.style.width = p1 + "%";
            f2Fill.style.width = p2 + "%";
        }, 80);

        resultSec.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function renderProfile(prefix, name, stats) {
        document.getElementById(`profile-${prefix}-name`).textContent = name;
        document.getElementById(`profile-${prefix}-record`).textContent = stats.record;

        const stanceEl = document.getElementById(`profile-${prefix}-stance`);
        const ageEl = document.getElementById(`profile-${prefix}-age`);
        stanceEl.textContent = stats.stance || "Unknown";
        ageEl.textContent = stats.age ? `Age ${stats.age}` : "";

        const grid = document.getElementById(`stats-${prefix}`);
        grid.innerHTML = "";

        const items = [
            ["Height", stats.height],
            ["Reach", stats.reach],
            ["Weight", stats.weight ? stats.weight + " lbs" : null],
            ["Win Streak", stats.currentWinStreak > 0 ? stats.currentWinStreak : "\u2014"],
            ["Sig. Str/Min", fmt(stats.avgSigStrLanded)],
            ["Str. Acc.", fmt(stats.avgSigStrPct, "%")],
            ["TD Avg", fmt(stats.avgTDLanded)],
            ["TD Acc.", fmt(stats.avgTDPct, "%")],
            ["Sub Avg", fmt(stats.avgSubAtt)],
            ["Title Bouts", fmt(stats.titleBouts)],
            ["Total Rnds", fmt(stats.totalRounds)],
            ["Best Streak", fmt(stats.longestWinStreak)],
        ];

        items.forEach(([label, value]) => {
            const div = document.createElement("div");
            div.className = "stat-item";
            div.innerHTML = `<span class="stat-label">${label}</span><span class="stat-value">${value || "\u2014"}</span>`;
            grid.appendChild(div);
        });
    }

    function renderComparison(name1, name2, f1, f2) {
        const rows = document.getElementById("comparison-rows");
        rows.innerHTML = "";

        const metrics = [
            ["Wins", f1.wins, f2.wins],
            ["Losses", f1.losses, f2.losses, true],
            ["Sig. Str/Min", f1.avgSigStrLanded, f2.avgSigStrLanded],
            ["Str. Accuracy", f1.avgSigStrPct, f2.avgSigStrPct],
            ["TD Average", f1.avgTDLanded, f2.avgTDLanded],
            ["TD Accuracy", f1.avgTDPct, f2.avgTDPct],
            ["Sub Attempts", f1.avgSubAtt, f2.avgSubAtt],
            ["Win Streak", f1.currentWinStreak, f2.currentWinStreak],
        ];

        metrics.forEach(([label, v1, v2, invertAdvantage]) => {
            const val1 = v1 ?? 0;
            const val2 = v2 ?? 0;
            const total = val1 + val2 || 1;
            const pct1 = (val1 / total) * 100;
            const pct2 = (val2 / total) * 100;

            const leftLeads = invertAdvantage ? val1 < val2 : val1 > val2;
            const rightLeads = invertAdvantage ? val2 < val1 : val2 > val1;

            const row = document.createElement("div");
            row.className = "cmp-row";
            row.innerHTML = `
                <div class="cmp-val left ${leftLeads ? 'advantage' : ''}">${fmt(v1)}</div>
                <div class="cmp-center">
                    <div class="cmp-label">${label}</div>
                    <div class="cmp-bar-wrap">
                        <div class="cmp-bar-left ${leftLeads ? 'lead' : ''}" style="width:${pct1}%"></div>
                        <div class="cmp-bar-right ${rightLeads ? 'lead' : ''}" style="width:${pct2}%"></div>
                    </div>
                </div>
                <div class="cmp-val right ${rightLeads ? 'advantage' : ''}">${fmt(v2)}</div>
            `;
            rows.appendChild(row);
        });
    }

    function renderMethods(f1, f2) {
        const methods = [
            ["KO/TKO", f1.koWins, f2.koWins],
            ["Submission", f1.subWins, f2.subWins],
            ["Decision", f1.decWins, f2.decWins],
        ];

        const maxVal = Math.max(...methods.flatMap(([, a, b]) => [a || 0, b || 0]), 1);

        const colF1 = document.getElementById("method-f1");
        const colF2 = document.getElementById("method-f2");
        const labels = document.getElementById("method-labels");
        colF1.innerHTML = "";
        colF2.innerHTML = "";
        labels.innerHTML = "";

        methods.forEach(([label, v1, v2]) => {
            const w1 = Math.max(((v1 || 0) / maxVal) * 100, 3);
            const w2 = Math.max(((v2 || 0) / maxVal) * 100, 3);

            labels.innerHTML += `<div class="method-row-label">${label}</div>`;

            colF1.innerHTML += `
                <div class="method-bar-wrap left">
                    <div class="method-bar red-bar" style="width:${w1}%">
                        <span class="method-count">${v1 || 0}</span>
                    </div>
                </div>`;

            colF2.innerHTML += `
                <div class="method-bar-wrap right">
                    <div class="method-bar blue-bar" style="width:${w2}%">
                        <span class="method-count">${v2 || 0}</span>
                    </div>
                </div>`;
        });
    }
});
