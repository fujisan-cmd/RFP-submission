/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // ConceptCraft カラーテーマ（ビジネスライク＆モダン）
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',  // メインブルー（信頼感のある企業カラー）
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        accent: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',  // モダンなグレイッシュブルー
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        innovation: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',  // イノベーション感のある紫
          600: '#9333ea',
          700: '#7c3aed',
          800: '#6b21a8',
          900: '#581c87',
        },
        success: {
          50: '#ecfdf5',
          500: '#10b981',  // 成功のエメラルドグリーン
          600: '#059669',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',  // 警告のアンバー
          600: '#d97706',
        },
        danger: {
          50: '#fef2f2',
          500: '#ef4444',  // エラーのレッド
          600: '#dc2626',
        }
      },
      backgroundImage: {
        'primary-gradient': 'linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%)',
        'accent-gradient': 'linear-gradient(135deg, #64748b 0%, #334155 100%)',
        'innovation-gradient': 'linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)',
      },
      boxShadow: {
        'modern': '0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'modern-lg': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      }
    },
  },
  plugins: [],
}