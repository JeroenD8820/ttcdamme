/**
 * TTC Damme - WVL158 Dashboard Logic
 */

class DataProvider {
    constructor() {
        this.data = null;
        this.calendars = null;
        this.matchDetails = null;
    }

    async init(seasonId = '26_27') {
        try {
            // Read from global variables populated by data.js or data_25_26.js
            let statsRes, calendarsRes, detailsRes;

            if (seasonId === '25_26' && window.DATA_25_26) {
                statsRes = window.DATA_25_26.PLAYER_STATS || [];
                calendarsRes = window.DATA_25_26.TEAM_CALENDARS || {};
                detailsRes = window.DATA_25_26.MATCH_DETAILS || {};
            } else {
                statsRes = window.PLAYER_STATS || [];
                calendarsRes = window.TEAM_CALENDARS || {};
                detailsRes = window.MATCH_DETAILS || {};
            }

            this.calendars = calendarsRes;
            this.matchDetails = detailsRes;

            // Prepare players data
            const players = Array.isArray(statsRes) ? statsRes.map(p => ({
                memberId: p.memberId,
                frenoyId: p.frenoyId,
                name: p.name,
                classification: p.classification,
                elo: p.elo,
                relative: p.relative
            })) : [];

            // Hardcoded basic rankings (kept consistent with current state)
            let rankings = [];
            let fullRankings = {};

            if (seasonId === '25_26') {
                rankings = [
                    { team: "Damme A", division: "1ste Provinciale A", position: 6, matches: 15, points: 31 },
                    { team: "Damme B", division: "3de Provinciale C", position: 10, matches: 15, points: 19 },
                    { team: "Damme C", division: "4de Provinciale B", position: 5, matches: 15, points: 31 },
                    { team: "Damme D", division: "4de Provinciale A", position: 7, matches: 15, points: 30 }
                ];

                fullRankings = {
                "Damme A": [
                    { "position": "1", "team": "T.T.C. Drive Oostende A", "matches": "15", "wins": "13", "losses": "0", "draws": "2", "points": "43" },
                    { "position": "2", "team": "T.T.C. Jong Gullegem D", "matches": "15", "wins": "11", "losses": "3", "draws": "1", "points": "38" },
                    { "position": "3", "team": "T.T.C. And Leie B", "matches": "15", "wins": "11", "losses": "3", "draws": "1", "points": "38" },
                    { "position": "4", "team": "TTC Mandelhoek A", "matches": "15", "wins": "10", "losses": "3", "draws": "2", "points": "37" },
                    { "position": "5", "team": "T.T.C. Wielsbeke-spotit B", "matches": "15", "wins": "8", "losses": "6", "draws": "1", "points": "32" },
                    { "position": "6", "team": "T.T.C. Damme A", "matches": "15", "wins": "6", "losses": "5", "draws": "4", "points": "31" },
                    { "position": "7", "team": "T.T.C. Torhout A", "matches": "15", "wins": "6", "losses": "8", "draws": "1", "points": "28" },
                    { "position": "8", "team": "K.T.T.C. Oostduinkerke B", "matches": "15", "wins": "5", "losses": "7", "draws": "3", "points": "28" },
                    { "position": "9", "team": "T.T.C. Eendracht Kuurne A", "matches": "15", "wins": "5", "losses": "9", "draws": "1", "points": "26" },
                    { "position": "10", "team": "T.T.C. Zandvoorde D", "matches": "15", "wins": "3", "losses": "11", "draws": "1", "points": "22" },
                    { "position": "11", "team": "T.T.C. Drive Oostende B", "matches": "15", "wins": "2", "losses": "12", "draws": "1", "points": "19" },
                    { "position": "12", "team": "T.T.C. Meulebeke A", "matches": "15", "wins": "0", "losses": "13", "draws": "2", "points": "17" }
                ],
                "Damme B": [
                    { "position": "1", "team": "T.T.C. Tielt A", "matches": "15", "wins": "15", "losses": "0", "draws": "0", "points": "45" },
                    { "position": "2", "team": "T.T.C. Koekelare B", "matches": "15", "wins": "12", "losses": "1", "draws": "2", "points": "41" },
                    { "position": "3", "team": "T.T.C. Drive Oostende D", "matches": "15", "wins": "13", "losses": "2", "draws": "0", "points": "40" },
                    { "position": "4", "team": "T.T.C. Knokke-Heist A", "matches": "15", "wins": "9", "losses": "5", "draws": "1", "points": "34" },
                    { "position": "5", "team": "T.T.C. And Leie D", "matches": "15", "wins": "8", "losses": "6", "draws": "1", "points": "32" },
                    { "position": "6", "team": "T.T.C. Zandvoorde H", "matches": "15", "wins": "7", "losses": "6", "draws": "2", "points": "30" },
                    { "position": "7", "team": "T.T.C. Wielsbeke-spotit F", "matches": "15", "wins": "7", "losses": "7", "draws": "1", "points": "30" },
                    { "position": "8", "team": "T.T.C. Jabbeke C", "matches": "15", "wins": "6", "losses": "9", "draws": "0", "points": "27" },
                    { "position": "9", "team": "T.T.C. Jong Gullegem G", "matches": "15", "wins": "5", "losses": "9", "draws": "1", "points": "26" },
                    { "position": "10", "team": "T.T.C. Damme B", "matches": "15", "wins": "2", "losses": "13", "draws": "0", "points": "19" },
                    { "position": "11", "team": "TTC Mandelhoek D", "matches": "15", "wins": "1", "losses": "14", "draws": "0", "points": "17" },
                    { "position": "12", "team": "T.T.C. Nieuwpoort B", "matches": "15", "wins": "1", "losses": "14", "draws": "0", "points": "17" }
                ],
                "Damme C": [
                    { "position": "1", "team": "T.T.C. Torhout D", "matches": "15", "wins": "14", "losses": "1", "draws": "0", "points": "43" },
                    { "position": "2", "team": "T.T.C. The Charlies B", "matches": "15", "wins": "13", "losses": "2", "draws": "0", "points": "40" },
                    { "position": "3", "team": "T.T.C. Koekelare D", "matches": "15", "wins": "8", "losses": "5", "draws": "2", "points": "33" },
                    { "position": "4", "team": "T.T.C. Damme C", "matches": "15", "wins": "8", "losses": "6", "draws": "1", "points": "32" },
                    { "position": "5", "team": "T.T.C. Jabbeke D", "matches": "15", "wins": "6", "losses": "5", "draws": "4", "points": "31" },
                    { "position": "6", "team": "T.T.C. Drive Oostende H", "matches": "15", "wins": "7", "losses": "7", "draws": "1", "points": "30" },
                    { "position": "7", "team": "T.T.C. Wielsbeke-spotit G", "matches": "15", "wins": "6", "losses": "7", "draws": "2", "points": "29" },
                    { "position": "8", "team": "T.T.C. Zonnebeke E", "matches": "15", "wins": "5", "losses": "6", "draws": "4", "points": "29" },
                    { "position": "9", "team": "T.T.C. Zandvoorde I", "matches": "15", "wins": "5", "losses": "10", "draws": "0", "points": "25" },
                    { "position": "10", "team": "K.T.T.C. Dino Brugge E", "matches": "15", "wins": "5", "losses": "10", "draws": "0", "points": "25" },
                    { "position": "11", "team": "T.T.C. Oostkamp C", "matches": "15", "wins": "3", "losses": "11", "draws": "1", "points": "21" },
                    { "position": "12", "team": "K.T.T.C. Oostduinkerke F", "matches": "15", "wins": "2", "losses": "12", "draws": "1", "points": "20" }
                ],
                "Damme D": [
                    { "position": "1", "team": "K.T.T.C. Oostduinkerke E", "matches": "15", "wins": "12", "losses": "3", "draws": "0", "points": "39" },
                    { "position": "2", "team": "T.T.C. Oostkamp B", "matches": "15", "wins": "10", "losses": "4", "draws": "1", "points": "36" },
                    { "position": "3", "team": "T.T.C. Drive Oostende G", "matches": "15", "wins": "10", "losses": "5", "draws": "0", "points": "35" },
                    { "position": "4", "team": "K.T.T.C. Dino Brugge D", "matches": "15", "wins": "8", "losses": "4", "draws": "3", "points": "34" },
                    { "position": "5", "team": "T.T.C. Knokke-Heist B", "matches": "15", "wins": "7", "losses": "6", "draws": "2", "points": "31" },
                    { "position": "6", "team": "T.T.C. De woudpalet Houthulst vzw C", "matches": "15", "wins": "8", "losses": "6", "draws": "1", "points": "31" },
                    { "position": "7", "team": "T.T.C. Damme D", "matches": "15", "wins": "7", "losses": "7", "draws": "1", "points": "30" },
                    { "position": "8", "team": "T.T.C. Meulebeke D", "matches": "15", "wins": "6", "losses": "7", "draws": "2", "points": "29" },
                    { "position": "9", "team": "T.T.C. Torhout E", "matches": "15", "wins": "7", "losses": "8", "draws": "0", "points": "28" },
                    { "position": "10", "team": "T.T.C. Zandvoorde J", "matches": "15", "wins": "6", "losses": "9", "draws": "0", "points": "27" },
                    { "position": "11", "team": "T.T.C. Koekelare E", "matches": "15", "wins": "3", "losses": "12", "draws": "0", "points": "20" },
                    { "position": "12", "team": "T.T.C. Bredene A", "matches": "15", "wins": "1", "losses": "14", "draws": "0", "points": "15" }
                ]
                };
            } else {
                // Seizoen 26-27 is nog niet gestart, dus geen rankings
                rankings = [];
                fullRankings = {};
            }

            // Recente Resultaten (Last played matches from all calendars)
            const allPlayed = [];
            Object.values(this.calendars).forEach(teamMatches => {
                teamMatches.forEach(m => {
                    if (m.score && m.score.includes('-')) allPlayed.push(m);
                });
            });

            // Helper to parse "Za 13-09-25" into Date object for sorting
            const parseVTTLDate = (dStr) => {
                if (!dStr || dStr === 'TBD') return new Date(0);
                const parts = dStr.split(' ');
                if (parts.length < 2) return new Date(0);
                const [d, m, y] = parts[1].split('-');
                return new Date(2000 + parseInt(y), parseInt(m) - 1, parseInt(d));
            };

            // Recente Resultaten (Last played match for EVERY team)
            const results = [];
            Object.entries(this.calendars).forEach(([teamLetter, teamMatches]) => {
                const played = teamMatches
                    .filter(m => m.score && m.score.includes('-'))
                    .sort((a, b) => parseVTTLDate(b.date) - parseVTTLDate(a.date));

                if (played.length > 0) {
                    const m = played[0];
                    results.push({
                        team: `Damme ${teamLetter}`,
                        date: m.date,
                        home: m.home_team,
                        away: m.away_team,
                        score: m.score,
                        matchId: m.match_id,
                        result: m.home_team.includes('Damme') ?
                            (parseInt(m.score.split('-')[0]) > parseInt(m.score.split('-')[1]) ? 'win' :
                                (parseInt(m.score.split('-')[0]) < parseInt(m.score.split('-')[1]) ? 'loss' : 'draw')) :
                            (parseInt(m.score.split('-')[1]) > parseInt(m.score.split('-')[0]) ? 'win' :
                                (parseInt(m.score.split('-')[1]) < parseInt(m.score.split('-')[0]) ? 'loss' : 'draw'))
                    });
                }
            });

            // Sort results by date so the newest ones are at the top
            results.sort((a, b) => parseVTTLDate(b.date) - parseVTTLDate(a.date));

            this.data = {
                players,
                rankings,
                results,
                fullRankings
            };
            return this.data;
        } catch (e) {
            console.error("Error loading data:", e);
            return null;
        }
    }
}

class Dashboard {
    constructor() {
        this.provider = new DataProvider();
        this.allPlayers = [];
        this.filteredPlayers = [];
        this.fullRankings = {};
        this.calendars = {};
        this.matchDetails = {};
        this.activeTeamPast = 'A';
        this.activeTeamUpcoming = 'A';
        this.init();
    }

    async init(seasonId = '26_27') {
        console.log("Initializing Dashboard for season:", seasonId);
        const data = await this.provider.init(seasonId);
        if (data) {
            this.allPlayers = data.players;
            
            // Apply any active filters if changing seasons
            const searchInput = document.getElementById('player-search');
            if (searchInput && searchInput.value) {
                const q = searchInput.value.toLowerCase();
                this.filteredPlayers = this.allPlayers.filter(p =>
                    p.name.toLowerCase().includes(q) ||
                    p.memberId.includes(q)
                );
            } else {
                this.filteredPlayers = [...this.allPlayers];
            }
            
            const sortSelect = document.getElementById('player-sort');
            if (sortSelect && sortSelect.value !== 'elo') {
                 // Sort logic is simple so we can just call it (though it re-renders inside, we do full render later)
                 // actually, just sorting the array is enough
                 const criteria = sortSelect.value;
                 this.filteredPlayers.sort((a, b) => {
                    if (criteria === 'elo') return b.elo - a.elo;
                    if (criteria === 'relative') return b.relative - a.relative;
                    if (criteria === 'name') return a.name.localeCompare(b.name);
                    if (criteria === 'classification') return a.classification.localeCompare(b.classification);
                    return 0;
                });
            }

            this.fullRankings = data.fullRankings;
            this.calendars = this.provider.calendars;
            this.matchDetails = this.provider.matchDetails;

            this.render(data);
            
            if (!this.eventsBound) {
                this.setupEventListeners();
                this.eventsBound = true;
            }
        }
    }

    setupEventListeners() {
        const searchInput = document.getElementById('player-search');
        const sortSelect = document.getElementById('player-sort');
        const seasonSelector = document.getElementById('season-selector');
        const closeBtns = document.querySelectorAll('.close-btn');
        const rankingModal = document.getElementById('ranking-modal');
        const matchModal = document.getElementById('match-modal');
        const opponentModal = document.getElementById('opponent-modal');
        const tabBtns = document.querySelectorAll('.tab-btn');
        const collapsibles = document.querySelectorAll('.collapsible-header');

        if (seasonSelector) {
            seasonSelector.addEventListener('change', (e) => {
                this.init(e.target.value);
            });
        }

        searchInput.addEventListener('input', (e) => {
            // Auto-expand members section when user starts typing
            const playersSection = document.getElementById('players');
            if (e.target.value && playersSection.classList.contains('collapsed')) {
                playersSection.classList.remove('collapsed');
            }
            this.filterPlayers(e.target.value);
        });
        sortSelect.addEventListener('change', (e) => this.sortPlayers(e.target.value));

        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                rankingModal.style.display = 'none';
                matchModal.style.display = 'none';
                opponentModal.style.display = 'none';
            });
        });

        window.addEventListener('click', (e) => {
            if (e.target === rankingModal) rankingModal.style.display = 'none';
            if (e.target === matchModal) matchModal.style.display = 'none';
            if (e.target === opponentModal) opponentModal.style.display = 'none';
        });

        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = btn.dataset.type;
                const team = btn.dataset.team;

                // Update active team based on section
                const section = btn.closest('.glass-section');

                // Auto-expand section if collapsed
                if (section.classList.contains('collapsed')) {
                    section.classList.remove('collapsed');
                }

                const btns = section.querySelectorAll('.tab-btn');
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                if (type === 'past') {
                    this.activeTeamPast = team;
                    this.renderPastCalendar();
                } else {
                    this.activeTeamUpcoming = team;
                    this.renderUpcomingCalendar();
                }
            });
        });

        collapsibles.forEach(header => {
            header.addEventListener('click', () => {
                const section = header.closest('.glass-section');
                section.classList.toggle('collapsed');
            });
        });

        // Refresh button - three scenarios:
        // 1. GitHub Pages (github.io) → data wordt automatisch door GitHub Actions bijgewerkt
        // 2. localhost → Flask server aanroepen voor live update
        // 3. file:// → probeer localhost:5000, anders herladen
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', async () => {
                const isGitHubPages = window.location.hostname.includes('github.io');
                const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                const isFile = window.location.protocol === 'file:';

                // --- GitHub Pages: data wordt automatisch bijgewerkt door GitHub Actions ---
                if (isGitHubPages) {
                    refreshBtn.disabled = true;
                    refreshBtn.classList.add('spinning');
                    this.showToast('🔄 Nieuwste data laden van GitHub...', 'info', 2000);
                    setTimeout(() => {
                        location.reload(true); // force reload, skip cache
                    }, 1200);
                    setTimeout(() => {
                        refreshBtn.disabled = false;
                        refreshBtn.classList.remove('spinning');
                    }, 2000);
                    return;
                }

                // --- Localhost of file:// → probeer Flask server ---
                const serverUrl = isFile ? 'http://localhost:5000' : '';
                refreshBtn.disabled = true;
                refreshBtn.classList.add('spinning');

                try {
                    const triggerRes = await fetch(`${serverUrl}/api/update`, {
                        method: 'POST',
                        signal: AbortSignal.timeout(3000)
                    });

                    if (!triggerRes.ok) throw new Error('Server fout');

                    this.showToast('⏳ Data ophalen van VTTL... (±2 min)', 'info', 120000);

                    // Poll until done
                    let done = false;
                    let attempts = 0;
                    while (!done && attempts < 120) {
                        await new Promise(r => setTimeout(r, 2000));
                        attempts++;
                        const statusRes = await fetch(`${serverUrl}/api/update/status`);
                        const status = await statusRes.json();
                        if (!status.running) {
                            done = true;
                            if (status.result && status.result.success) {
                                this.showToast(`✅ Data bijgewerkt om ${status.result.timestamp}`, 'success');
                                setTimeout(() => location.reload(), 1500);
                            } else {
                                const errLog = status.result ? status.result.logs.join('\n') : 'Onbekende fout';
                                this.showToast('❌ Update mislukt. Zie console voor details.', 'error');
                                console.error('Update logs:', errLog);
                            }
                        }
                    }

                    if (!done) {
                        this.showToast('⚠️ Timeout: update duurt te lang.', 'error');
                    }
                } catch (e) {
                    // Flask server niet actief → gewoon herladen
                    this.showToast('🔄 Pagina herladen...', 'info', 2000);
                    setTimeout(() => location.reload(), 1500);
                } finally {
                    refreshBtn.disabled = false;
                    refreshBtn.classList.remove('spinning');
                }
            });
        }
    }

    filterPlayers(query) {
        const q = query.toLowerCase();
        this.filteredPlayers = this.allPlayers.filter(p =>
            p.name.toLowerCase().includes(q) ||
            p.memberId.includes(q)
        );
        this.renderPlayers();
    }

    sortPlayers(criteria) {
        this.filteredPlayers.sort((a, b) => {
            if (criteria === 'elo') return b.elo - a.elo;
            if (criteria === 'relative') return b.relative - a.relative;
            if (criteria === 'name') return a.name.localeCompare(b.name);
            if (criteria === 'classification') return a.classification.localeCompare(b.classification);
            return 0;
        });
        this.renderPlayers();
    }

    showRankingDetails(teamName) {
        const ranking = this.fullRankings[teamName];
        if (!ranking) return;

        const modal = document.getElementById('ranking-modal');
        const title = document.getElementById('modal-title');
        const body = document.getElementById('modal-table-body');

        title.textContent = `Rangschikking ${teamName}`;
        body.innerHTML = '';

        ranking.forEach(item => {
            const tr = document.createElement('tr');
            if (item.team.includes('Damme')) tr.className = 'highlight-row';

            tr.innerHTML = `
                <td>${item.position}</td>
                <td style="text-align: left">${item.team}</td>
                <td>${item.matches}</td>
                <td>${item.wins}</td>
                <td>${item.losses}</td>
                <td>${item.draws}</td>
                <td><strong>${item.points}</strong></td>
            `;
            body.appendChild(tr);
        });

        modal.style.display = 'block';
    }

    showMatchDetail(matchId) {
        const detail = this.matchDetails[matchId];
        if (!detail) {
            console.warn("No details found for match:", matchId);
            return;
        }

        const modal = document.getElementById('match-modal');

        // Find match in calendar to get teams/score info
        let matchInfo = null;
        Object.values(this.calendars).forEach(list => {
            const found = list.find(m => m.match_id === matchId);
            if (found) matchInfo = found;
        });

        document.getElementById('match-home-team').textContent = matchInfo ? matchInfo.home_team : "Thuis";
        document.getElementById('match-away-team').textContent = matchInfo ? matchInfo.away_team : "Bezoekers";
        document.getElementById('match-overall-score').textContent = matchInfo ? matchInfo.score : "-";

        const homePlayersList = document.getElementById('match-home-players');
        homePlayersList.innerHTML = detail.home_players.map(p => `
            <li>
                <div class="player-info">
                    <span class="p-name">${p.name}</span>
                    <span class="p-class">${p.classification}</span>
                </div>
                <span class="p-won">${p.won}</span>
            </li>
        `).join('');

        const awayPlayersList = document.getElementById('match-away-players');
        awayPlayersList.innerHTML = detail.away_players.map(p => `
            <li>
                <div class="player-info">
                    <span class="p-name">${p.name}</span>
                    <span class="p-class">${p.classification}</span>
                </div>
                <span class="p-won">${p.won}</span>
            </li>
        `).join('');

        const gamesBody = document.getElementById('match-games-body');
        gamesBody.innerHTML = detail.games.map(g => `
            <tr>
                <td>${g.home_player}</td>
                <td>${g.away_player}</td>
                <td>
                    <strong>${g.result_sets}</strong>
                    <span class="set-scores">${g.sets}</span>
                </td>
                <td><strong>${g.result_game}</strong></td>
            </tr>
        `).join('');

        modal.style.display = 'block';
    }

    render(data) {
        this.renderRankings(data.rankings);
        this.renderResults(data.results);
        this.renderPlayers();
        this.renderPastCalendar();
        this.renderUpcomingCalendar();
        document.getElementById('rankings-timestamp').textContent = new Date().toLocaleTimeString();
    }

    renderPlayers() {
        const body = document.getElementById('players-body');
        if (!body) return;
        body.innerHTML = '';

        this.filteredPlayers.forEach(p => {
            const tr = document.createElement('tr');
            const relClass = p.relative > 0 ? 'rel-pos' : (p.relative < 0 ? 'rel-neg' : 'rel-zero');
            const relText = p.relative > 0 ? `+${p.relative}` : p.relative;

            tr.innerHTML = `
                <td>${p.name}</td>
                <td>${p.classification}</td>
                <td><span class="elo-val">${p.elo}</span></td>
                <td><span class="${relClass}">${relText}</span></td>
                <td>
                    <a href="https://competitie.vttl.be/index.php?menu=6&sel=${p.frenoyId}&result=1" target="_blank" class="btn-icon">VTTL</a>
                </td>
            `;
            body.appendChild(tr);
        });
    }

    renderRankings(rankings) {
        const grid = document.getElementById('rankings-grid');
        if (!grid) return;
        grid.innerHTML = '';

        rankings.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>${item.team}</h3>
                <div class="division">${item.division}</div>
                <div class="rank-info">
                    <div class="position">#${item.position}</div>
                    <div class="points">
                        <span class="val">${item.points} pt</span>
                        <span class="label">${item.matches} matchen</span>
                    </div>
                </div>
            `;
            card.addEventListener('click', () => this.showRankingDetails(item.team));
            grid.appendChild(card);
        });
    }

    renderResults(results) {
        const body = document.getElementById('results-body');
        if (!body) return;
        body.innerHTML = '';

        results.forEach(res => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${res.date}</td>
                <td>${res.home}</td>
                <td>${res.away}</td>
                <td class="${res.result}">${res.score}</td>
            `;
            if (res.matchId) {
                tr.style.cursor = 'pointer';
                tr.addEventListener('click', () => this.showMatchDetail(res.matchId));
            }
            body.appendChild(tr);
        });
    }

    showOpponentHistory(teamName) {
        // Get all matches for this opponent across all divisions
        const opponentMatches = [];

        Object.entries(this.calendars).forEach(([team, matches]) => {
            matches.forEach(match => {
                if ((match.home_team === teamName || match.away_team === teamName) && match.score && match.score.includes('-')) {
                    opponentMatches.push(match);
                }
            });
        });

        // Sort by date (most recent first)
        opponentMatches.sort((a, b) => {
            const dateA = this.parseVTTLDate(a.date);
            const dateB = this.parseVTTLDate(b.date);
            return dateB - dateA;
        });

        // Display in modal
        const modal = document.getElementById('opponent-modal');
        const teamNameEl = document.getElementById('opponent-team-name');
        const tbody = document.getElementById('opponent-history-body');

        teamNameEl.textContent = teamName;
        tbody.innerHTML = '';

        opponentMatches.forEach(match => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';

            // Get player info if available
            const matchDetail = this.matchDetails[match.match_id];
            let playersInfo = '-';
            if (matchDetail) {
                const homePlayers = matchDetail.home_players.map(p => p.name).join(', ');
                const awayPlayers = matchDetail.away_players.map(p => p.name).join(', ');
                playersInfo = `<small>${match.home_team}: ${homePlayers}<br>${match.away_team}: ${awayPlayers}</small>`;
            }

            tr.innerHTML = `
                <td>${match.date}</td>
                <td>${match.home_team}</td>
                <td>${match.away_team}</td>
                <td><strong>${match.score}</strong></td>
                <td>${playersInfo}</td>
            `;

            // Click to view match detail
            if (match.url && matchDetail) {
                tr.addEventListener('click', () => this.showMatchDetail(match.match_id));
            }

            tbody.appendChild(tr);
        });

        modal.style.display = 'block';
    }

    renderPastCalendar() {
        const body = document.getElementById('calendar-past-body');
        if (!body) return;
        const matches = (this.calendars[this.activeTeamPast] || []).filter(m => m.score && m.score.includes('-'));

        const parseVTTLDate = (dStr) => {
            if (!dStr || dStr === 'TBD') return new Date(0);
            const parts = dStr.split(' ');
            if (parts.length < 2) return new Date(0);
            const [d, m, y] = parts[1].split('-');
            return new Date(2000 + parseInt(y), parseInt(m) - 1, parseInt(d));
        };

        // Sort New to Old
        matches.sort((a, b) => parseVTTLDate(b.date) - parseVTTLDate(a.date));

        body.innerHTML = '';
        matches.forEach(m => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${m.date}</td>
                <td>${m.time}</td>
                <td>${m.home_team}</td>
                <td>${m.away_team}</td>
                <td class="score-cell">${m.score}</td>
            `;

            // Add click handler ONLY to the score cell for match details
            if (m.url) {
                const scoreCell = tr.querySelector('.score-cell');
                scoreCell.style.cursor = 'pointer';
                scoreCell.addEventListener('click', () => {
                    this.showMatchDetail(m.match_id);
                });
            }

            body.appendChild(tr);
        });
    }

    renderUpcomingCalendar() {
        const body = document.getElementById('calendar-upcoming-body');
        if (!body) return;

        // allMatches: not yet played (no score) — filtered further by date below
        const allMatches = (this.calendars[this.activeTeamUpcoming] || []).filter(m => !m.score || !m.score.includes('-'));
        const dammeTeamName = `Damme ${this.activeTeamUpcoming}`;

        const parseVTTLDate = (dStr) => {
            if (!dStr || dStr === 'TBD') return new Date(0);
            const parts = dStr.split(' ');
            if (parts.length < 2) return new Date(0);
            const [d, m, y] = parts[1].split('-');
            return new Date(2000 + parseInt(y), parseInt(m) - 1, parseInt(d));
        };

        // Only show matches in the future (date >= today)
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const matches = allMatches.filter(m => {
            if (!m.home_team.includes(dammeTeamName) && !m.away_team.includes(dammeTeamName)) return false;
            const matchDate = parseVTTLDate(m.date);
            return matchDate >= today;
        });

        matches.sort((a, b) => parseVTTLDate(a.date) - parseVTTLDate(b.date));

        body.innerHTML = '';

        // If no upcoming matches, show a season-transition message
        if (matches.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td colspan="5" style="text-align:center; padding: 2rem; opacity: 0.6; font-style: italic;">
                📅 Geen komende wedstrijden gevonden.<br>
                <small>Het seizoen 2025-2026 is afgelopen. De kalender voor 2026-2027 is nog niet beschikbaar.</small>
            </td>`;
            body.appendChild(tr);
            return;
        }

        matches.forEach(m => {
            const tr = document.createElement('tr');

            // Determine which team is the opponent
            const isDammeHome = m.home_team.includes(dammeTeamName);
            // const opponentTeam = isDammeHome ? m.away_team : m.home_team; // This variable is not used in the provided snippet, so I'll omit it.

            // Make only the opponent team name clickable
            const homeTeamHtml = isDammeHome ? m.home_team : `<span class="clickable-team" data-team="${m.home_team}">${m.home_team}</span>`;
            const awayTeamHtml = isDammeHome ? `<span class="clickable-team" data-team="${m.away_team}">${m.away_team}</span>` : m.away_team;

            tr.innerHTML = `
                <td>${m.date}</td>
                <td>${m.time}</td>
                <td>${homeTeamHtml}</td>
                <td>${awayTeamHtml}</td>
                <td>${m.score || '-'}</td>
            `;

            // Add click handler only to opponent team name
            tr.querySelectorAll('.clickable-team').forEach(span => {
                span.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.showOpponentHistory(span.dataset.team);
                });
            });

            body.appendChild(tr);
        });
    }
    showToast(message, type = 'info', duration = 4000) {
        // Remove existing toast
        const existing = document.getElementById('ttc-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'ttc-toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
            background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : 'rgba(255,255,255,0.15)'};
            color: white; padding: 12px 24px; border-radius: 12px;
            backdrop-filter: blur(12px); font-size: 0.95rem; font-weight: 600;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 9999;
            border: 1px solid rgba(255,255,255,0.2); white-space: nowrap;
            animation: toastIn 0.3s ease;
        `;

        if (!document.getElementById('ttc-toast-style')) {
            const style = document.createElement('style');
            style.id = 'ttc-toast-style';
            style.textContent = `
                @keyframes toastIn { from { opacity:0; transform: translateX(-50%) translateY(20px); } to { opacity:1; transform: translateX(-50%) translateY(0); } }
                .refresh-btn.spinning i { animation: spin 0.8s linear infinite; }
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(toast);
        if (duration < 60000) {
            setTimeout(() => toast.remove(), duration);
        }
    }
}

// Start the app
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});
