// =======================
// Chat Platform DBML - dbdiagram.io compatible
// Fully comprehensive, scalable, E2EE-ready
// =======================

// ---------- Core user & auth ----------
Table users {
id uuid [pk]
username varchar(64) [unique, not null]
normalized_username varchar(64) [unique]
email varchar(255) [unique]
phone varchar(32) [unique]
display_name varchar(128)
about text
avatar_url text
password_hash varchar(255)
salt varchar(128)
locale varchar(16)
timezone varchar(64)
is_active boolean [default: true]
is_bot boolean [default: false]
metadata jsonb [note: "arbitrary profile metadata"]
created_at timestamp
updated_at timestamp
deleted_at timestamp
}

Table user_profiles {
user_id uuid [pk, ref: > users.id]
profile_json jsonb
updated_at timestamp
}

// ---------- Sessions, tokens & oauth ----------
Table user_sessions {
id uuid [pk]
user_id uuid [ref: > users.id]
session_token varchar(255) [unique]
device_id uuid [ref: > devices.id]
ip varchar(64)
user_agent text
created_at timestamp
last_seen timestamp
expires_at timestamp
revoked boolean [default: false]
}

Table refresh_tokens {
id uuid [pk]
user_id uuid [ref: > users.id]
token_hash varchar(255)
device_id uuid [ref: > devices.id]
created_at timestamp
revoked_at timestamp
expires_at timestamp
}

Table oauth_providers {
id uuid [pk]
user_id uuid [ref: > users.id]
provider varchar(64)
provider_user_id varchar(255)
raw_profile jsonb
created_at timestamp
unique (provider, provider_user_id)
}

// ---------- Devices & push ----------
Table devices {
id uuid [pk]
user_id uuid [ref: > users.id]
device_id varchar(255)
device_name varchar(128)
platform varchar(32)
push_token text
app_version varchar(64)
last_seen timestamp
created_at timestamp
revoked boolean [default: false]
unique (user_id, device_id)
}

Table push_notifications {
id uuid [pk]
user_id uuid [ref: > users.id]
device_id uuid [ref: > devices.id]
title varchar(255)
body text
payload jsonb
provider_response jsonb
status varchar(32) [default: 'pending']
retry_count int [default: 0]
sent_at timestamp
created_at timestamp
}

// ---------- Identity & E2EE key material ----------
Table identity_keys {
user_id uuid [pk, ref: > users.id]
identity_pubkey text
identity_algo varchar(64) [default: 'ed25519']
signed_prekey_id int
signed_prekey_pub text
signed_prekey_sig text
signed_prekey_created timestamp
prekey_count int [default: 0]
metadata jsonb
created_at timestamp
updated_at timestamp
}

Table one_time_prekeys {
id uuid [pk]
user_id uuid [ref: > users.id]
prekey_id int
prekey_pub text
created_at timestamp
used boolean [default: false]
used_at timestamp
unique (user_id, prekey_id)
}

Table device_keys {
device_id uuid [pk, ref: > devices.id]
device_pubkey text
key_algo varchar(64) [default: 'x25519']
signed_by_identity text
created_at timestamp
revoked_at timestamp
}

// ---------- Contacts & social graph ----------
Table contacts {
id uuid [pk]
owner_id uuid [ref: > users.id]
contact_user_id uuid [ref: > users.id]
alias varchar(128)
is_blocked boolean [default: false]
is_favorite boolean [default: false]
created_at timestamp
updated_at timestamp
unique (owner_id, contact_user_id)
}

Table blocks {
id uuid [pk]
blocker_id uuid [ref: > users.id]
blocked_id uuid [ref: > users.id]
reason varchar(256)
created_at timestamp
unique (blocker_id, blocked_id)
}

// ---------- Conversations & membership ----------
Table conversations {
id uuid [pk]
type varchar(16) [default: 'direct']
title varchar(255)
topic varchar(255)
avatar_url text
creator_id uuid [ref: > users.id]
visibility varchar(16) [default: 'members']
member_count int [default: 0]
last_message_id uuid [ref: - messages.id]
created_at timestamp
updated_at timestamp
archived boolean [default: false]
metadata jsonb
}

Table conversation_members {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
user_id uuid [ref: > users.id]
role varchar(16) [default: 'member']
joined_at timestamp
left_at timestamp
is_muted boolean [default: false]
unread_count int [default: 0]
last_read_message_id uuid [ref: - messages.id]
last_read_at timestamp
last_important_message_id uuid [ref: - messages.id]
unique (conversation_id, user_id)
}

Table conversation_settings {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
key varchar(128)
value jsonb
unique (conversation_id, key)
}

// ---------- Messages & attachments ----------
Table messages {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
sender_id uuid [ref: > users.id]
ciphertext text [note: "Base64 AEAD ciphertext"]
ciphertext_nonce varchar(128)
encryption_algo varchar(64) [default: 'xchacha20_poly1305']
sender_ephemeral_pub text
signature text
message_type varchar(32) [default: 'text']
preview_text_hash varchar(128)
is_edited boolean [default: false]
edit_history jsonb
is_deleted boolean [default: false]
deleted_at timestamp
send_status varchar(32) [default: 'queued']
created_at timestamp
updated_at timestamp
metadata jsonb
}

Table message_participants_cache {
message_id uuid [pk, ref: > messages.id]
participant_ids jsonb [note: "Array of participant UUIDs"]
created_at timestamp
}

// ---------- Per-recipient encrypted CEKs ----------
Table message_encrypted_keys {
id uuid [pk]
message_id uuid [ref: > messages.id]
recipient_user_id uuid [ref: > users.id]
recipient_device_id uuid [ref: > devices.id]
encrypted_key text
key_algo varchar(64) [default: 'x25519-aead']
nonce varchar(128)
created_at timestamp
unique (message_id, recipient_user_id, recipient_device_id)
}

// ---------- Media stores & attachments ----------
Table media_stores {
id uuid [pk]
provider varchar(64)
bucket varchar(255)
object_key text
url text
storage_class varchar(64)
metadata jsonb
created_at timestamp
}

Table message_attachments {
id uuid [pk]
message_id uuid [ref: > messages.id]
storage_id uuid [ref: > media_stores.id]
encrypted boolean [default: true]
file_name_enc varchar(255)
file_size bigint
mime_type varchar(128)
width int
height int
duration_seconds int
checksum varchar(128)
encryption_meta jsonb
created_at timestamp
}

// ---------- Delivery & read status ----------
Table message_status {
id uuid [pk]
message_id uuid [ref: > messages.id]
user_id uuid [ref: > users.id]
status varchar(32) [default: 'sent']
status_at timestamp
device_id uuid [ref: > devices.id]
platform varchar(32)
created_at timestamp
unique (message_id, user_id)
}

Table read_receipts_summary {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
message_id uuid [ref: > messages.id]
delivered_count int [default: 0]
seen_count int [default: 0]
updated_at timestamp
unique (conversation_id, message_id)
}

// ---------- Reactions, pins, starred, edits ----------
Table message_reactions {
id uuid [pk]
message_id uuid [ref: > messages.id]
user_id uuid [ref: > users.id]
reaction varchar(64)
reacted_at timestamp
unique (message_id, user_id, reaction)
}

Table pinned_items {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
message_id uuid [ref: > messages.id]
pinned_by uuid [ref: > users.id]
pinned_at timestamp
expires_at timestamp
}

Table starred_messages {
id uuid [pk]
user_id uuid [ref: > users.id]
message_id uuid [ref: > messages.id]
starred_at timestamp
unique (user_id, message_id)
}

Table message_edit_history {
id uuid [pk]
message_id uuid [ref: > messages.id]
editor_id uuid [ref: > users.id]
previous_body_hash varchar(128)
previous_ciphertext text
edited_at timestamp
}

// ---------- Drafts & scheduled messages ----------
Table message_drafts {
id uuid [pk]
user_id uuid [ref: > users.id]
conversation_id uuid [ref: > conversations.id]
draft_text_enc text
attachments jsonb
updated_at timestamp
}

Table scheduled_messages {
id uuid [pk]
message_payload jsonb
conversation_id uuid [ref: > conversations.id]
scheduled_time timestamp
created_by uuid [ref: > users.id]
status varchar(32)
run_at timestamp
created_at timestamp
}

// ---------- Moderation & reports ----------
Table reports {
id uuid [pk]
reporter_id uuid [ref: > users.id]
target_type varchar(64)
target_id uuid
reason varchar(256)
details text
status varchar(32)
assigned_to uuid [ref: > users.id]
created_at timestamp
updated_at timestamp
}

Table bans {
id uuid [pk]
user_id uuid [ref: > users.id]
banned_by uuid [ref: > users.id]
reason varchar(256)
expires_at timestamp
created_at timestamp
}

// ---------- Key backups ----------
Table key_backups {
id uuid [pk]
user_id uuid [ref: > users.id]
backup_blob text
version varchar(64)
created_at timestamp
updated_at timestamp
}

// ---------- Call logs ----------
Table call_logs {
id uuid [pk]
conversation_id uuid [ref: > conversations.id]
caller_id uuid [ref: > users.id]
callee_id uuid [ref: > users.id]
started_at timestamp
ended_at timestamp
call_type varchar(16)
status varchar(32)
metadata jsonb
created_at timestamp
}

// =======================
// End of dbdiagram.io compatible schema
// =======================
