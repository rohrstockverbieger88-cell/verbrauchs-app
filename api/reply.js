const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  const { to, subject, message, includeSignature } = req.body;

  if (!to || !message) {
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
    const finalMessage = includeSignature !== false 
        ? `${message}\n\n---\nViele Grüße,\nDein Metraxo Team`
        : message;

    await transporter.sendMail({
      from: process.env.GMX_EMAIL,
      to: to,
      subject: `RE: ${subject || 'Metraxo Anfrage'}`,
      text: finalMessage
    });

    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Mail reply error:', error);
    res.status(500).json({ success: false, error: 'Fehler beim Senden der Antwort-E-Mail' });
  }
}
