import { useState } from 'react';
import {
  FolderKanban, Plus, Clock, CheckCircle2, Circle, AlertTriangle,
  TrendingUp, Users, Calendar, Target, Zap
} from 'lucide-react';

type TaskStatus = 'todo' | 'in_progress' | 'review' | 'done';
type Priority = 'high' | 'medium' | 'low';

interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  priority: Priority;
  assignee: string;
  dueDate: string;
  progress: number;
  tags: string[];
}

const columns: { key: TaskStatus; label: string; color: string; bg: string }[] = [
  { key: 'todo', label: 'لم تبدأ', color: 'text-gray-500', bg: 'bg-gray-100' },
  { key: 'in_progress', label: 'قيد التنفيذ', color: 'text-blue-600', bg: 'bg-blue-50' },
  { key: 'review', label: 'مراجعة', color: 'text-amber-600', bg: 'bg-amber-50' },
  { key: 'done', label: 'مكتملة', color: 'text-green-600', bg: 'bg-green-50' },
];

const tasks: Task[] = [
  { id: 1, title: 'تطوير موديل AI للتنبؤ بالمبيعات', status: 'in_progress', priority: 'high', assignee: 'فريق التقنية', dueDate: '20 يونيو', progress: 65, tags: ['AI', 'تطوير'] },
  { id: 2, title: 'عرض STC Solutions - المرحلة 2', status: 'review', priority: 'high', assignee: 'أحمد', dueDate: '18 يونيو', progress: 90, tags: ['مبيعات', 'STC'] },
  { id: 3, title: 'تحديث واجهة المستخدم الرئيسية', status: 'in_progress', priority: 'medium', assignee: 'فريق التصميم', dueDate: '25 يونيو', progress: 40, tags: ['تصميم', 'UI'] },
  { id: 4, title: 'تحليل بيانات Q2 للمستثمرين', status: 'todo', priority: 'high', assignee: 'المالية', dueDate: '30 يونيو', progress: 0, tags: ['مالية', 'تقارير'] },
  { id: 5, title: 'إعداد عرض المستشفى الوطني', status: 'in_progress', priority: 'medium', assignee: 'خالد', dueDate: '22 يونيو', progress: 55, tags: ['مبيعات', 'صحة'] },
  { id: 6, title: 'تحسين أداء قاعدة البيانات', status: 'todo', priority: 'low', assignee: 'فريق التقنية', dueDate: '28 يونيو', progress: 10, tags: ['تقنية', 'تحسين'] },
  { id: 7, title: 'عقد نيوم التقنية - توقيع', status: 'done', priority: 'high', assignee: 'بدر', dueDate: '15 يونيو', progress: 100, tags: ['مبيعات', 'نيوم'] },
  { id: 8, title: 'ورشة عمل فريق المبيعات', status: 'done', priority: 'medium', assignee: 'الفريق', dueDate: '10 يونيو', progress: 100, tags: ['تدريب', 'فريق'] },
];

const projects = [
  { name: 'توسعة STC', progress: 78, tasks: 12, completed: 9, color: 'bg-blue-500' },
  { name: 'القطاع الصحي', progress: 45, tasks: 8, completed: 3, color: 'bg-green-500' },
  { name: 'تحديث المنصة', progress: 32, tasks: 15, completed: 4, color: 'bg-purple-500' },
  { name: 'تقرير المستثمرين', progress: 90, tasks: 5, completed: 4, color: 'bg-amber-500' },
];

export default function ProjectsPage() {
  const [draggedTask, setDraggedTask] = useState<number | null>(null);
  const [taskList, setTaskList] = useState(tasks);

  const handleDrop = (status: TaskStatus) => {
    if (draggedTask === null) return;
    setTaskList(prev => prev.map(t =>
      t.id === draggedTask ? { ...t, status, progress: status === 'done' ? 100 : t.progress } : t
    ));
    setDraggedTask(null);
  };

  const totalTasks = taskList.length;
  const completedTasks = taskList.filter(t => t.status === 'done').length;
  const inProgressTasks = taskList.filter(t => t.status === 'in_progress').length;
  const highPriorityTasks = taskList.filter(t => t.priority === 'high' && t.status !== 'done').length;

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">إدارة المشاريع والمهام</h1>
          <p className="text-sm text-gray-500 mt-1">نظام Kanban لتتبع المشاريع والمهام</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest text-sm font-bold">
          <Plus className="w-4 h-4" /> مهمة جديدة
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <FolderKanban className="w-5 h-5 text-dealix-emerald" />
            <span className="text-sm text-gray-500">إجمالي المهام</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{totalTasks}</p>
          <p className="text-xs text-gray-400 mt-1">في جميع الأعمدة</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="w-5 h-5 text-green-500" />
            <span className="text-sm text-gray-500">مكتملة</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{completedTasks}</p>
          <p className="text-xs text-green-600 mt-1">{Math.round((completedTasks / totalTasks) * 100)}% من الإجمالي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-blue-500" />
            <span className="text-sm text-gray-500">قيد التنفيذ</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{inProgressTasks}</p>
          <p className="text-xs text-blue-600 mt-1">نشطة حالياً</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <span className="text-sm text-gray-500">أولوية عالية</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{highPriorityTasks}</p>
          <p className="text-xs text-red-600 mt-1">تتطلب اهتمام</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Kanban Board */}
        <div className="lg:col-span-3">
          <div className="grid grid-cols-4 gap-3">
            {columns.map((col) => {
              const colTasks = taskList.filter(t => t.status === col.key);
              return (
                <div
                  key={col.key}
                  className="bg-gray-50 rounded-xl p-3 min-h-[500px]"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={() => handleDrop(col.key)}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      {col.key === 'todo' ? <Circle className={`w-4 h-4 ${col.color}`} /> :
                       col.key === 'in_progress' ? <Zap className={`w-4 h-4 ${col.color}`} /> :
                       col.key === 'review' ? <Clock className={`w-4 h-4 ${col.color}`} /> :
                       <CheckCircle2 className={`w-4 h-4 ${col.color}`} />}
                      <span className={`text-sm font-bold ${col.color}`}>{col.label}</span>
                    </div>
                    <span className="text-xs text-gray-400 bg-white px-2 py-0.5 rounded-full">{colTasks.length}</span>
                  </div>

                  <div className="space-y-2">
                    {colTasks.map((task) => (
                      <div
                        key={task.id}
                        draggable
                        onDragStart={() => setDraggedTask(task.id)}
                        className="bg-white rounded-lg p-3 shadow-sm border border-gray-100 cursor-move hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                            task.priority === 'high' ? 'bg-red-100 text-red-600' :
                            task.priority === 'medium' ? 'bg-amber-100 text-amber-600' :
                            'bg-green-100 text-green-600'
                          }`}>
                            {task.priority === 'high' ? 'عالية' : task.priority === 'medium' ? 'متوسطة' : 'منخفضة'}
                          </span>
                          {task.status === 'done' && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                        </div>
                        <p className="text-sm font-bold text-gray-900 mb-2">{task.title}</p>
                        <div className="flex items-center gap-1 flex-wrap mb-2">
                          {task.tags.map((tag, i) => (
                            <span key={i} className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{tag}</span>
                          ))}
                        </div>
                        <div className="flex items-center justify-between text-xs text-gray-400">
                          <div className="flex items-center gap-1">
                            <Users className="w-3 h-3" />
                            <span>{task.assignee}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            <span>{task.dueDate}</span>
                          </div>
                        </div>
                        {task.status !== 'done' && task.status !== 'todo' && (
                          <div className="mt-2">
                            <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                              <div className="h-full bg-dealix-emerald rounded-full transition-all" style={{ width: `${task.progress}%` }} />
                            </div>
                            <p className="text-[10px] text-gray-400 mt-0.5 text-left">{task.progress}%</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-6">
          {/* Projects Progress */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <h3 className="font-bold text-gray-900 mb-4">تقدم المشاريع</h3>
            <div className="space-y-4">
              {projects.map((project, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-800">{project.name}</span>
                    <span className="text-xs text-gray-500">{project.completed}/{project.tasks}</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full ${project.color} rounded-full transition-all`} style={{ width: `${project.progress}%` }} />
                  </div>
                  <p className="text-[10px] text-gray-400 mt-1">{project.progress}% مكتمل</p>
                </div>
              ))}
            </div>
          </div>

          {/* Team Workload */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <h3 className="font-bold text-gray-900 mb-4">تحميل الفريق</h3>
            <div className="space-y-3">
              {['أحمد', 'خالد', 'فهد', 'بدر'].map((name, i) => {
                const count = taskList.filter(t => t.assignee.includes(name) || (i === 3 && t.assignee === 'بدر')).length;
                const workload = [75, 60, 85, 45][i];
                return (
                  <div key={name} className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-dealix-emerald to-dealix-forest flex items-center justify-center text-white text-xs font-bold">
                      {name[0]}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-800">{name}</span>
                        <span className="text-xs text-gray-400">{count} مهام</span>
                      </div>
                      <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden mt-1">
                        <div className={`h-full rounded-full ${workload > 80 ? 'bg-red-400' : workload > 60 ? 'bg-amber-400' : 'bg-green-400'}`} style={{ width: `${workload}%` }} />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-gradient-to-br from-dealix-emerald to-dealix-forest rounded-xl p-5 text-white">
            <h3 className="font-bold mb-3">إجراءات سريعة</h3>
            <div className="space-y-2">
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-white/10 rounded-lg text-sm hover:bg-white/20 transition-colors">
                <Target className="w-4 h-4" /> هدف جديد للفريق
              </button>
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-white/10 rounded-lg text-sm hover:bg-white/20 transition-colors">
                <TrendingUp className="w-4 h-4" /> تقرير تقدم
              </button>
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-white/10 rounded-lg text-sm hover:bg-white/20 transition-colors">
                <Users className="w-4 h-4" /> توزيع مهام
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
