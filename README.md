# פרויקט במדעי הרוח הדיגיטליים
## מטרת הפרויקט: 
פרויקט זה עוסק בשילוב נשים כדמויות ראשיות בעולם הקולנוע במדינות שונות ברחבי העולם.
המטרה העיקרית של הפרויקט הינה לבדוק מהו היחס בין נשים לגברים בתפקידים ראשים וכן לראות האם יש הבדל בין המדינות השונות. 
יתר על כן, נבדוק אילו תפקידים נשים מגלמות כדמויות ראשיות לעומת התפקידים אשר גברים מגלמים. נרצה לבדוק האם יש הנחה סטראוטיפית אשר עומדת מאחורי בחירת התפקידים עבור נשים וגברים. בנוסף, נבדוק האם ניכרים שינויים, והאם יש עליה בכמות השחקניות בתפקידים ראשיים לאורך השנים.
הפרויקט מתמקד בסרטים רבים המתועדים ב- IMDB וב-TMDB  שיצאו בין השנים 1960-2022 במדינות שונות ברחבי העולם. 

## רקע- הקשר למדעי הרוח הדיגיטליים:
עולם הקולנוע הוא אחד מתחומי האומנות הפופולריים ביותר, המהווה חלק בלתי נפרד מתחום מדעי הרוח הדיגיטליים.
הפרויקט שלנו ישלב כרייה של נתונים ממקורות מידע רבים ומגוונים, ניתוח המידע וחילוץ מידע רלוונטי עבור צרכי הפרויקט.
לאחר איסוף הנתונים נבצע הסקת מסקנות וכן נצליב מידע על מנת להציג את התוצאות באמצעות כלי דיגיטלי אשר יראה את ההבדלים בין גברים לנשים מכמה היבטים בעולם הקולנוע.
באמצעות כלי זה נספק מידע עשיר ומגוון אודות שאלת המחקר שלנו בצורה קלה וברורה. 

## תכנית העבודה :
הפרויקט ייכתב בשפת python. 
נשתמש במאגרי הנתונים מ-IMDB ומ-TMDB. באמצעות ה-API של IMDB נקבל את כל הסרטים בין השנים 1960-2022 עבור מספר רב של מדינות אשר משקפות תרבויות שונות ברחבי העולם. כמו כן, באמצעות API של TMDB נשלוף מידע נוסף על הדמות הראשית של כל סרט (כגון: מין, שם הדמות וכדומה). כלל מידע זה נשמור בקבצי json. 
נבצע בדיקה אלו תפקידים ראשיים נוטות נשים לגלם ואילו תפקידים ראשיים נוטים גברים לגלם. 
ננסה לשלוף מידע זה באמצעות עלילת הסרט או באמצעות תיאור הדמות (אשר מופיע ב-IMDB).
תוצאות העבודה יוצגו בצורה ויזואלית אשר ימחישו בצורה קלה וברורה את ההבדלים השונים בין גברים לנשים. ככל הנראה נציג את הממצאים באמצעות גרפים, דיאגרמות ומפות. 

## היעד:
•	אחוזי גברים מול נשים בתפקידים ראשיים: אנו מצפות שהיחס בתפקידים ראשיים יטה לכיוון הגברים. בסרטים ישנים נצפה לראות יחס יותר קיצוני ומובהק אך לקראת שנים מתקדמות יותר היחס יצטמצם. למרות השינוי בין השנים, הגברים ימשיכו להוות רוב, ותמיד תהיה שאיפה מצד הנשים להגיע לשוויון . 
לפי ממצאים שפורסמו בכתבה בעיתון "הארץ", התברר כי "בשנת 2007 רק 24% מהסרטים כללו נשים בתפקידים ראשיים ואילו ב–2019 זינק המספר ל–48%. נתון זה מרשים עוד יותר לאור העובדה שמדובר בבדיקת 100 הסרטים הרווחיים ביותר של השנה, כך שאפשר לקבוע כי הקהל שמח לראות סרטים בהובלת נשים. מנהלי האולפנים בהוליווד מגלים באיחור ניכר שנשים יכולות לשאת על גבן סרטים, ושסיפורים על נשים יכולים לסחוף את הקהל, נשים וגברים כאחד". מתוך ידיעה זו אנו מצפות להגיע ליעד שתיארנו לעיל.

•	אחוזי גברים מול נשים בתפקידים ראשיים בין המדינות השונות: כפי שצוין לעיל, אנו מצפות לראות יחס לא שוויוני בגילום תפקידים ראשיים בין נשים לגברים. בנוסף, אנו מצפות לראות יחס זה בצורה חדה יותר במדינות פחות מודרניות שבהן הנשים זוכות ליחס פחות שוויוני (כגון מצרים).

•	תפקידי נשים מול תפקידי גברים: אנו מצפות לראות כי תפקידי המינים השונים יהיו מותאמים לסטריאוטיפים הרווחים בחברה. גברים יקבלו תפקידים המעידים על כוח, גבורה וחוכמה. לעומת זאת, נשים יקבלו תפקידים נחותים ובעלי אופי מיני. 
מסקנות הללו מתבססות על מאמרים שקראנו. במאמרים אלו עלו ממצאים מעניינים כגון: 
"עם זאת נראה כי העלייה בייצוג נשים מרמזת על דריכה סמויה במקום. דמויות של נשים בקולנוע הן עדיין בעלות סיכוי גדול פי 6 להיות מאופיינות על ידי מיניותן" (מתוך עיתון "הארץ" ),
" Studies from the past two decades have confirmed that women in the film industry are both underrepresented (University, 2017; Lauzen, 2018b) and portrayed stereotypically (Wood, 1994)"  (from the article " https://www.nature.com/articles/s41599-020-0436-1").

## מקורות ביבליוגרפים: 
1.	https://www.haaretz.co.il/gallery/opinion/2020-03-08/ty-article/.premium/0000017f-db6c-d3a5-af7f-fbee68270000
2.	https://www.nature.com/articles/s41599-020-0436-1
3.	https://developers.themoviedb.org/3/configuration/get-languages
4.	https://imdb-api.com/api/#Search-header


 
