const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  const { email, subject, message } = req.body;

  if (!email || !message) {
    return res.status(400).json({ message: 'Missing fields' });
  }

  const transporter = nodemailer.createTransport({
    host: 'mail.gmx.net',
    port: 465,
    secure: true,
    auth: {
      user: process.env.GMX_EMAIL,
      pass: process.env.GMX_PASSWORD
    }
  });

  try {
    await transporter.sendMail({
      from: process.env.GMX_EMAIL,
      to: process.env.GMX_EMAIL,
      replyTo: email,
      subject: `Metraxo Kontakt: ${subject}`,
      text: `Neue Nachricht über das Metraxo Kontaktformular:\n\nAbsender: ${email}\nBetreff: ${subject}\n\nNachricht:\n${message}`
    });

    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Mail error:', error);
    res.status(500).json({ success: false, error: 'Fehler beim Senden der E-Mail' });
  }
}
