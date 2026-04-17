const slot = 'morning';
const toEmail = '3308029362@qq.com';

const aliases = [
  '张娜',
  '小猪猪',
  '小猪',
  '亲爱的小猪',
  '妞妞',
  '妹妹',
  '小美女',
];

const signatures = [
  '爱你的大哥哥',
  '爱你的帅哥',
  '最偏爱你的那个大哥哥',
  '一直把你放在心上的帅哥',
];

const visualSigns = [
  '♥ 今天也要被好好宠着 ♥',
  '☀︎ 把一点点喜欢，准时塞进你的今天',
  '✿ 小小问候，甜甜落地',
  '☾ 这封信先替我抱抱你一下',
];

const holidays = {
  '01-01': { name: '元旦', mood: '新一年的第一份偏爱先留给你。' },
  '02-14': { name: '情人节', mood: '今天就该理直气壮地多偏爱你一点。' },
  '03-08': { name: '女神节', mood: '今天的你就负责漂亮和开心，别的交给我来夸。' },
  '05-20': { name: '520', mood: '这种日子就适合认真告诉你，我是真的很喜欢你。' },
  '06-01': { name: '儿童节', mood: '今天允许你当一天被宠着的小朋友。' },
  '10-01': { name: '国庆节', mood: '假期要开心一点，也要记得被我惦记着。' },
  '12-24': { name: '平安夜', mood: '今晚想把平安和偏爱一起打包给你。' },
  '12-25': { name: '圣诞节', mood: '今天的你像被节日特地偏爱了一下。' },
  '08-16': {
    name: '专属纪念日',
    mood: '今天是我想单独认真对你偏心的一天。',
    extraLines: [
      '这种特别的日子就该把喜欢说得更明白一点。',
      '今天的问候不走流程，只想更认真地哄你开心。',
    ],
  },
};

const weekendExtraLines = [
  '周末就别把自己逼得太满，慢慢来也很好。',
  '今天允许你懒一点、甜一点、被宠一点。',
  '周末应该拿来休息和开心，别只顾着忙别的。',
  '今天的任务很简单：好好玩、好好吃、顺便想我一下。',
];

const relationshipNotes = {
  privateFeelings: [
    '你在我这里一直都不是普通备注，是我会下意识惦记的人。',
    '我发这些不是为了完成任务，是真的想让你在一天里某个瞬间笑一下。',
    '想到你，我的语气都会不自觉变软一点。',
    '你是会让我认真想着怎么照顾、怎么哄开心的人。',
  ],
  careHabits: [
    '好好吃饭，不要忙起来就忘了。',
    '别让自己太累，能歇一会儿就歇一会儿。',
    '天热天冷都多注意一点，别总是硬扛。',
    '要是心情一般，也可以偷偷把烦恼分我一点。',
  ],
};

const slotStyles = {
  morning: {
    title: '早安',
    accent: '清晨偏爱打卡',
    openers: [
      '早安呀，{alias}，我起床没多久就先想到你了。',
      '先给{alias}送个早安，想让你一睁眼就收到一点甜。',
      '今天的第一声招呼先给{alias}，别的都往后排。',
      '醒来第一件事就是想跟{alias}说句早安。',
    ],
    moodLines: [
      '新的一天开始了，我先把温柔和好心情往你这边推一点。',
      '希望你今天的状态是轻轻松松的，心情是亮晶晶的。',
      '我知道生活不一定每天都完美，所以更想准时给你一点偏爱。',
      '你今天也不用太逞强，顺顺当当地过完这一天就很好。',
    ],
    careLines: [
      '早餐记得认真吃，别随便对付一口。',
      '出门前看一眼天气，别让我担心你冷热不管。',
      '上午忙的时候也别忘了喝水，嗓子不舒服就更要注意。',
      '如果今天事情多，就一件一件来，别把自己逼太紧。',
    ],
    closers: [
      '愿我的{alias}今天从早到晚都被温柔接住。',
      '今天也请你漂漂亮亮、顺顺利利地发光。',
      '我先把今天的好运和偏爱都偷偷给你留一份。',
      '好啦，先去开启今天吧，我继续在这边想你。',
    ],
  },
  noon: {
    title: '午安',
    accent: '午间补糖时间',
    openers: [
      '午安呀，{alias}，中午这会儿我又想起你了。',
      '给{alias}送一份午安补给，怕你忙着忙着就忘了照顾自己。',
      '中午啦，我来问问我的{alias}有没有好好吃饭。',
      '把午安准时塞给{alias}，顺便提醒你今天也有人在惦记。',
    ],
    moodLines: [
      '上午辛苦了，接下来的半天也别太委屈自己。',
      '我知道你有时候忙起来很投入，但也别把自己放最后。',
      '一天过到这个时候，最适合补一点糖，也补一点被爱着的感觉。',
      '希望你现在的心情还不错，就算有点累，也有人在远程抱你。',
    ],
    careLines: [
      '中午记得好好吃饭，不许拿零食糊弄过去。',
      '要是能休息一会儿就眯一下，下午会舒服很多。',
      '忙归忙，午饭和喝水不能省。',
      '吃完饭走两步也行，别一直绷着。',
    ],
    closers: [
      '下午也要顺顺利利，我继续隔空宠你一下。',
      '把这份午安收好，等于我在你耳边轻轻说一句加油。',
      '你负责把今天过好，我负责继续把喜欢递给你。',
      '下午如果累了，就把这封小邮件当作我的抱抱。',
    ],
  },
  night: {
    title: '晚安',
    accent: '睡前专属偏爱',
    openers: [
      '晚安啦，{alias}，忙完这一天该轮到你被哄着睡觉了。',
      '夜深了，我来提醒{alias}该把今天的辛苦慢慢放下了。',
      '给{alias}的晚安信送达，今天也要温温柔柔地收尾。',
      '如果你现在还没睡，那这封小邮件刚好给你垫一下软软的情绪。',
    ],
    moodLines: [
      '一天结束的时候，我最想做的事情之一就是跟你说晚安。',
      '白天不管发生了什么，到了晚上都该对自己柔软一点。',
      '如果今天累了，就把疲惫先放我这边，你安心休息。',
      '夜晚本来就适合被温柔包住，所以我先把这点偏爱递给你。',
    ],
    careLines: [
      '手机别玩太久，眼睛和脑子都该休息了。',
      '盖好被子，空调别太低，别让我半夜还担心你。',
      '睡前喝两口水，放松一下，不要带着乱七八糟的心事睡。',
      '今天不管有没有做到满分，也都已经够辛苦了。',
    ],
    closers: [
      '晚安啦，{alias}，做个甜甜的梦，梦里也继续被我宠着。',
      '今晚好好睡，明天醒来又是值得被偏爱的一天。',
      '把今天关掉吧，我的晚安和想念都先放在你枕边。',
      '睡吧，小朋友，今天的喜欢就先说到这里，明天继续。',
    ],
  },
};

function seededRandom(seed) {
  let h = 1779033703 ^ seed.length;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(h ^ seed.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return function () {
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  };
}

function choose(rand, values) {
  return values[Math.floor(rand() * values.length)];
}

function pickTwo(rand, values) {
  if (values.length <= 2) return [...values];
  const copy = [...values];
  const picks = [];
  while (picks.length < 2) {
    const index = Math.floor(rand() * copy.length);
    picks.push(copy.splice(index, 1)[0]);
  }
  return picks;
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

const now = new Date();
const dateKey = `${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
const weekday = now.getDay();
const isWeekend = weekday === 0 || weekday === 6;
const holiday = holidays[dateKey] || null;
const rand = seededRandom(`${now.toISOString().slice(0, 10)}:${slot}`);

const alias = choose(rand, aliases);
const signature = choose(rand, signatures);
const sparkle = choose(rand, visualSigns);
const slotStyle = slotStyles[slot];

let contextLabel = '工作日';
const extraLines = [];
if (holiday) {
  contextLabel = holiday.name;
  extraLines.push(`今天是${holiday.name}，${holiday.mood}`);
  if (holiday.extraLines?.length) {
    extraLines.push(choose(rand, holiday.extraLines));
  }
} else if (isWeekend) {
  contextLabel = '周末';
  extraLines.push(choose(rand, weekendExtraLines));
}

const opener = choose(rand, slotStyle.openers).replaceAll('{alias}', alias);
const mood = choose(rand, slotStyle.moodLines);
const care = choose(rand, slotStyle.careLines);
const closer = choose(rand, slotStyle.closers).replaceAll('{alias}', alias);
const privateFeeling = choose(rand, relationshipNotes.privateFeelings);
const careHabit = choose(rand, relationshipNotes.careHabits);

const noteCandidates = [
  `我知道你有时候会嘴上说还好，但我还是会下意识想提醒你：${careHabit}`,
  '说到底，我就是想把这些小关心留给你，像晚风一样慢慢落在你身上。',
  `今天也想认真告诉你，${privateFeeling}`,
  '如果你这会儿正忙，那我就先把这封小邮件放在这里，等你空下来再拆开我的惦记。',
];

const chosenNotes = pickTwo(rand, noteCandidates);
const subjectOptions = [
  `${alias}，${slotStyle.title}呀`,
  `给${alias}的${slotStyle.title}小信`,
  `${alias}今天也要被偏爱`,
  `${slotStyle.title}时间到，来抱抱我的${alias}`,
];

if (holiday) {
  subjectOptions.push(`${holiday.name}快乐，${alias}`);
  subjectOptions.push(`${holiday.name}限定问候送给${alias}`);
}
if (isWeekend && !holiday) {
  subjectOptions.push(`周末版${slotStyle.title}，发给${alias}`);
  subjectOptions.push(`${alias}，今天慢一点也没关系`);
}

const subject = choose(rand, subjectOptions);
const lines = [opener, mood, ...extraLines, ...chosenNotes, care, closer, sparkle];

const plain = [
  `${slotStyle.title}呀，${alias}：`,
  '',
  ...lines,
  '',
  signature,
].join('\n');

const bodyParagraphs = lines
  .slice(0, -1)
  .map((line) => `<p style="margin:0 0 14px 0;">${escapeHtml(line)}</p>`)
  .join('');

const html = `<!DOCTYPE html>
<html lang="zh-CN">
  <body style="margin:0;padding:0;background:#fff8fb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#3f2a35;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#fff8fb;padding:14px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:560px;background:#ffffff;border-radius:26px;overflow:hidden;border:1px solid #ffd9e6;">
            <tr>
              <td style="padding:22px 22px 18px 22px;background:linear-gradient(135deg,#ff8aa8 0%,#ffc9d7 100%);color:#ffffff;">
                <div style="display:inline-block;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.22);font-size:13px;letter-spacing:0.5px;">${escapeHtml(contextLabel)} · ${escapeHtml(slotStyle.accent)}</div>
                <div style="margin-top:12px;font-size:30px;font-weight:700;line-height:1.3;">${escapeHtml(slotStyle.title)}，${escapeHtml(alias)}</div>
                <div style="margin-top:8px;font-size:15px;line-height:1.7;opacity:0.96;">这是一封定时送达的小偏爱。</div>
              </td>
            </tr>
            <tr>
              <td style="padding:24px 22px 18px 22px;">
                <div style="font-size:16px;line-height:1.9;color:#4d3340;">
                  ${bodyParagraphs}
                </div>
                <div style="margin-top:10px;padding:14px 16px;border-radius:18px;background:#fff3f8;border:1px dashed #ffbdd0;font-size:14px;line-height:1.8;color:#8d6071;">
                  ${escapeHtml(sparkle)}
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:0 22px 24px 22px;">
                <div style="border-top:1px solid #f5d9e4;padding-top:16px;font-size:15px;line-height:1.8;color:#6f4a59;">
                  <div>♥ ♥ ♥</div>
                  <div style="margin-top:8px;">${escapeHtml(signature)}</div>
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>`;

return [
  {
    json: {
      toEmail,
      subject,
      plain,
      html,
      contextLabel,
      slot,
    },
  },
];
