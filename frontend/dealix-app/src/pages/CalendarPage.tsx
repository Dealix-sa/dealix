import { useState } from 'react';
import {
  ChevronRight, ChevronLeft, Clock, MapPin, Users, Phone,
  Video, Plus, Calendar as CalIcon, CheckCircle2
} from 'lucide-react';

const weekDays = ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'];

const timeSlots = [
  '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00',
];

const events = [
  { id: 1, day: 1, startSlot: 1, duration: 1, title: 'اجتماع مع STC Solutions', type: 'meeting', location: 'مكتب الرياض', attendees: ['فهد المطيري', 'محمد'], color: 'bg-dealix-emerald' },
  { id: 2, day: 1, startSlot: 3, duration: 1, title: 'مكالمة - العقارات الكبرى', type: 'call', location: 'هاتف', attendees: ['أحمد الشمري'], color: 'bg-blue-500' },
  { id: 3, day: 2, startSlot: 5, duration: 2, title: 'عرض المنتج - الصحة الوطني', type: 'presentation', location: 'فيديو', attendees: ['خالد العنزي', 'فريق المبيعات'], color: 'bg-purple-500' },
  { id: 4, day: 3, startSlot: 2, duration: 1, title: 'متابعة عرض نيوم', type: 'call', location: 'هاتف', attendees: ['بدر العتيبي'], color: 'bg-blue-500' },
  { id: 5, day: 3, startSlot: 7, duration: 1, title: 'اجتماع فريق المبيعات', type: 'meeting', location: 'المكتب', attendees: ['الفريق'], color: 'bg-amber-500' },
  { id: 6, day: 4, startSlot: 4, duration: 1, title: 'اجتماع مع المستثمرين', type: 'meeting', location: 'فيديو', attendees: ['مجموعة المستثمرين'], color: 'bg-red-500' },
  { id: 7, day: 5, startSlot: 1, duration: 1, title: 'مراجعة الأداء الأسبوعية', type: 'review', location: 'المكتب', attendees: ['الإدارة'], color: 'bg-dealix-gold' },
  { id: 8, day: 0, startSlot: 9, duration: 1, title: 'تخطيط الأسبوع القادم', type: 'planning', location: 'المكتب', attendees: ['فريق التخطيط'], color: 'bg-gray-500' },
];

const todayTasks = [
  { time: '09:00', title: 'اجتماع مع STC Solutions', done: true },
  { time: '11:00', title: 'مكالمة - العقارات الكبرى', done: false },
  { time: '14:00', title: 'مراجعة التقرير المالي', done: false },
  { time: '16:00', title: 'متابعة عرض نيوم', done: false },
];

export default function CalendarPage() {
  const [selectedDay, setSelectedDay] = useState(1);

  const todayEvents = events.filter(e => e.day === selectedDay);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">التقويم التنفيذي</h1>
          <p className="text-sm text-gray-500 mt-1">إدارة المواعيد والاجتماعات</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
            <ChevronRight className="w-4 h-4" /> الأسبوع السابق
          </button>
          <span className="px-4 py-2 bg-dealix-charcoal text-white rounded-lg text-sm font-bold">
            يونيو 2025 - الأسبوع الثالث
          </span>
          <button className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
            الأسبوع التالي <ChevronLeft className="w-4 h-4" />
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg text-sm font-bold">
            <Plus className="w-4 h-4" /> موعد جديد
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Calendar Grid */}
        <div className="lg:col-span-3 bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
          {/* Day Headers */}
          <div className="grid grid-cols-7 border-b border-gray-100">
            {weekDays.map((day, i) => (
              <button
                key={day}
                onClick={() => setSelectedDay(i)}
                className={`py-4 text-center transition-colors ${
                  selectedDay === i ? 'bg-dealix-emerald/5 border-b-2 border-dealix-emerald' : 'hover:bg-gray-50'
                }`}
              >
                <p className={`text-sm font-bold ${selectedDay === i ? 'text-dealix-emerald' : 'text-gray-900'}`}>{day}</p>
                <p className={`text-xs mt-1 ${selectedDay === i ? 'text-dealix-emerald' : 'text-gray-400'}`}>
                  {14 + i} يونيو
                </p>
                {events.filter(e => e.day === i).length > 0 && (
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-dealix-gold mt-1" />
                )}
              </button>
            ))}
          </div>

          {/* Time Grid */}
          <div className="grid grid-cols-7 divide-x divide-gray-50" style={{ direction: 'ltr' }}>
            {weekDays.map((_, dayIndex) => {
              const dayEvents = events.filter(e => e.day === dayIndex);
              return (
                <div key={dayIndex} className="relative min-h-[600px]">
                  {timeSlots.map((slot) => (
                    <div
                      key={slot}
                      className="h-[50px] border-b border-gray-50 hover:bg-gray-50/50 transition-colors"
                    />
                  ))}
                  {dayEvents.map((event) => (
                    <div
                      key={event.id}
                      onClick={() => setSelectedDay(dayIndex)}
                      className={`absolute left-1 right-1 ${event.color} rounded-lg p-2 text-white cursor-pointer hover:opacity-90 transition-opacity shadow-md`}
                      style={{
                        top: `${event.startSlot * 50 + 2}px`,
                        height: `${event.duration * 50 - 4}px`,
                      }}
                    >
                      <p className="text-[11px] font-bold leading-tight">{event.title}</p>
                      <p className="text-[9px] opacity-80 mt-0.5">{timeSlots[event.startSlot]}</p>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-6">
          {/* Today's Summary */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <div className="flex items-center gap-2 mb-4">
              <CalIcon className="w-5 h-5 text-dealix-emerald" />
              <h3 className="font-bold text-gray-900">ملخص اليوم</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">المواعيد</span>
                <span className="font-bold text-gray-900">{todayEvents.length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">اجتماعات</span>
                <span className="font-bold text-gray-900">{todayEvents.filter(e => e.type === 'meeting').length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">مكالمات</span>
                <span className="font-bold text-gray-900">{todayEvents.filter(e => e.type === 'call').length}</span>
              </div>
            </div>
          </div>

          {/* Selected Day Events */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <h3 className="font-bold text-gray-900 mb-4">مواعيد {weekDays[selectedDay]}</h3>
            {todayEvents.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-4">لا توجد مواعيد</p>
            ) : (
              <div className="space-y-3">
                {todayEvents.map((event) => (
                  <div key={event.id} className="flex gap-3 p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                    <div className={`w-2 rounded-full ${event.color} self-stretch`} />
                    <div className="flex-1">
                      <p className="text-sm font-bold text-gray-900">{event.title}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Clock className="w-3 h-3 text-gray-400" />
                        <span className="text-xs text-gray-500">{timeSlots[event.startSlot]}</span>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        {event.location === 'فيديو' ? <Video className="w-3 h-3 text-gray-400" /> :
                         event.location === 'هاتف' ? <Phone className="w-3 h-3 text-gray-400" /> :
                         <MapPin className="w-3 h-3 text-gray-400" />}
                        <span className="text-xs text-gray-500">{event.location}</span>
                      </div>
                      <div className="flex items-center gap-1 mt-1">
                        <Users className="w-3 h-3 text-gray-400" />
                        <span className="text-xs text-gray-500">{event.attendees.join(', ')}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Today's Tasks */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <h3 className="font-bold text-gray-900 mb-4">مهام اليوم</h3>
            <div className="space-y-3">
              {todayTasks.map((task, i) => (
                <div key={i} className="flex items-center gap-3">
                  <button className="shrink-0">
                    <CheckCircle2 className={`w-5 h-5 ${task.done ? 'text-green-500' : 'text-gray-300'}`} />
                  </button>
                  <div className="flex-1">
                    <p className={`text-sm ${task.done ? 'line-through text-gray-400' : 'text-gray-800 font-medium'}`}>{task.title}</p>
                    <p className="text-xs text-gray-400">{task.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
