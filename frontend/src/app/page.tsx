import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="mt-6 text-center">
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
            ConceptCraft
          </h1>
          <p className="text-sm text-slate-600 mt-1 font-medium">by tantan</p>
        </div>
        <p className="mt-4 text-center text-lg text-slate-700 font-medium">
          新規事業開発のアイデア精緻化をサポート
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10 border border-slate-200">
          <div className="space-y-4">
            <Link
              href="/signup"
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:scale-105"
            >
              新規登録
            </Link>
            
            <Link
              href="/login"
              className="w-full flex justify-center py-3 px-4 border border-slate-300 rounded-md shadow-sm bg-white text-sm font-medium text-slate-700 hover:bg-slate-50 hover:border-blue-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all"
            >
              ログイン
            </Link>
          </div>
          
          <div className="mt-8 text-center">
            <h2 className="text-lg font-medium text-slate-900 mb-4">
              主な機能
            </h2>
            <ul className="text-sm text-slate-700 space-y-2">
              <li className="flex items-center justify-center space-x-2">
                <span className="text-purple-500">✓</span>
                <span>生成AIとの壁打ち機能</span>
              </li>
              <li className="flex items-center justify-center space-x-2">
                <span className="text-purple-500">✓</span>
                <span>リーンキャンバスの作成・更新</span>
              </li>
              <li className="flex items-center justify-center space-x-2">
                <span className="text-purple-500">✓</span>
                <span>インタラクティブな事業企画支援</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
