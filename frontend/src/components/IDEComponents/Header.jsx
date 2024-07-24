
const Header = () => {
  return (
    <header className="flex justify-between items-center p-4 bg-[#13002B]">
      <h1 className="text-xl">CustomCode IDE</h1>
      <div className="space-x-4">
        <button title="Open File" className="text-xl">📂</button>
        <button title="Save File" className="text-xl">💾</button>
        <button title="Reload" className="text-xl">🔄</button>
        <button title="Settings" className="text-xl">⚙️</button>
      </div>
    </header>
  );
};

export default Header;
