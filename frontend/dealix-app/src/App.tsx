import { HashRouter, Routes, Route } from 'react-router-dom';
import DashboardLayout from '@/layouts/DashboardLayout';
import CockpitPage from '@/pages/CockpitPage';
import CommandRoomPage from '@/pages/CommandRoomPage';
import WarRoomPage from '@/pages/WarRoomPage';
import EvidenceBoardPage from '@/pages/EvidenceBoardPage';
import ApprovalsPage from '@/pages/ApprovalsPage';
import MarketingOpsPage from '@/pages/MarketingOpsPage';
import SalesOpsPage from '@/pages/SalesOpsPage';
import StrategyPage from '@/pages/StrategyPage';
import FinancialPage from '@/pages/FinancialPage';
import AnalyticsPage from '@/pages/AnalyticsPage';
import SettingsPage from '@/pages/SettingsPage';
import TargetingPage from '@/pages/TargetingPage';
import DraftsHubPage from '@/pages/DraftsHubPage';
import ReportsPage from '@/pages/ReportsPage';
import CrmPage from '@/pages/CrmPage';
import CalendarPage from '@/pages/CalendarPage';
import ProjectsPage from '@/pages/ProjectsPage';
import InvestorPage from '@/pages/InvestorPage';
import NotificationsPage from '@/pages/NotificationsPage';

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<CockpitPage />} />
          <Route path="/cockpit" element={<CockpitPage />} />
          <Route path="/command-room" element={<CommandRoomPage />} />
          <Route path="/war-room" element={<WarRoomPage />} />
          <Route path="/evidence" element={<EvidenceBoardPage />} />
          <Route path="/approvals" element={<ApprovalsPage />} />
          <Route path="/marketing" element={<MarketingOpsPage />} />
          <Route path="/sales" element={<SalesOpsPage />} />
          <Route path="/strategy" element={<StrategyPage />} />
          <Route path="/financial" element={<FinancialPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/targeting" element={<TargetingPage />} />
          <Route path="/drafts" element={<DraftsHubPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/crm" element={<CrmPage />} />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/investor" element={<InvestorPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}

export default App;
