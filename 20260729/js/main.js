/**
 * 銀河軟體 教學專區 - 主頁卡片互動與搜尋腳本
 * Author: Falo x Force Cheng
 * Date: 2026-07-28
 * Description: 支援標籤篩選、關鍵字搜尋、LocalStorage 完成度狀態，以及全卡片新視窗 (target="_blank") 連結開啟。
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const tagButtons = document.querySelectorAll('.tag-btn');
  const cards = document.querySelectorAll('.topic-card');

  let activeCategory = 'all';

  // 確保首頁所有卡片連結按鈕皆設定為新視窗開啟 (target="_blank")
  const cardBtns = document.querySelectorAll('.card-btn');
  cardBtns.forEach(btn => {
    btn.setAttribute('target', '_blank');
    btn.setAttribute('rel', 'noopener noreferrer');
  });

  // 搜尋與過濾功能
  function filterCards() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    cards.forEach(card => {
      const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
      const desc = card.querySelector('.card-desc')?.textContent.toLowerCase() || '';
      const category = card.dataset.category || '';

      const matchesSearch = title.includes(query) || desc.includes(query);
      const matchesCategory = (activeCategory === 'all') || (category === activeCategory);

      if (matchesSearch && matchesCategory) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  // 搜尋輸入監聽
  if (searchInput) {
    searchInput.addEventListener('input', filterCards);
  }

  // 分類 Tag 點擊監聽
  tagButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tagButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.dataset.category || 'all';
      filterCards();
    });
  });

  // 載入與切換閱讀標記狀態 (LocalStorage)
  function initCompletionStatus() {
    const completedTopics = JSON.parse(localStorage.getItem('erp_completed_topics') || '[]');

    cards.forEach(card => {
      const topicId = card.dataset.topicId;
      const toggleBtn = card.querySelector('.complete-toggle');

      if (topicId && toggleBtn) {
        if (completedTopics.includes(topicId)) {
          toggleBtn.classList.add('completed');
          toggleBtn.title = '已完成學習 (點擊切換)';
          toggleBtn.innerHTML = '✓ 已完成';
        } else {
          toggleBtn.classList.remove('completed');
          toggleBtn.title = '標記為已完成';
          toggleBtn.innerHTML = '○ 未完成';
        }

        toggleBtn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();

          let list = JSON.parse(localStorage.getItem('erp_completed_topics') || '[]');
          if (list.includes(topicId)) {
            list = list.filter(id => id !== topicId);
          } else {
            list.push(topicId);
          }
          localStorage.setItem('erp_completed_topics', JSON.stringify(list));
          initCompletionStatus();
        });
      }
    });
  }

  initCompletionStatus();
});
